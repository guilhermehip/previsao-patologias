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
        pivot_df = df.groupBy("id_paciente", "idade", "sexo", "patologia").pivot("questao").agg(F.first("alternativa").alias("alternativa"))

        pivot_df.na.fill(value=0)
        
        pivot_df = pivot_df.repartition(100)
        pivot_df.write \
            .format("parquet") \
            .mode("overwrite") \
            .option("path", './app/storage/parquet/dataframe_modelo.parquet') \
            .save()
