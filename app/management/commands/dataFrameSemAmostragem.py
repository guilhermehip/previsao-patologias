from django.core.management.base import BaseCommand
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Crie uma sessão do Spark
        spark = SparkSession.builder.appName("Pivotar Dataframe do Modelo") \
            .config("spark.jars", "./app/storage/drivers/postgresql-42.7.1.jar") \
            .config("spark.sql.debug.maxToStringFields", 1000) \
            .getOrCreate()
        
        # Converta o esquema do DataFrame
        df = spark.read.parquet("./app/storage/parquet/ficha_clinica_estruturada.parquet")
        pivot_df = df.groupBy("id_paciente", "idade", "sexo", "patologia", "severidade", "evidencia_inicial").pivot("questao").agg(F.first("alternativa").alias("alternativa"))

        # Renomear todas as colunas para o formato desejado
        for c in pivot_df.columns:
            if c not in ["id_paciente", "idade", "sexo", "patologia", "evidencia_inicial"]:
                nome_coluna_tratado = c.replace(" ", "_").replace(".", "").replace("?", "").lower()
                pivot_df = pivot_df.withColumnRenamed(c, nome_coluna_tratado)
        
        # Preencher valores nulos com 0
        pivot_df = pivot_df.fillna(0)
        
        # Reparticionar o DataFrame
        pivot_df = pivot_df.repartition(100)

        # Salvar o DataFrame pivoteado no formato parquet
        pivot_df.write \
            .format("parquet") \
            .mode("overwrite") \
            .option("path", './app/storage/parquet/dataframe_modelo.parquet') \
            .save()
