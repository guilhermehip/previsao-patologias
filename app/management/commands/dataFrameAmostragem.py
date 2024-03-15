from django.core.management.base import BaseCommand
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Crie uma sessão do Spark
        spark = SparkSession.builder.appName("Pivotar Dataframe do Modelo") \
            .config("spark.jars", "./app/storage/drivers/postgresql-42.7.1.jar") \
            .config("spark.sql.debug.maxToStringFields", 1000) \
            .getOrCreate()
        
        # Seleciona todas as colunas binárias     
        query = "select texto from tb_questoes tq where tipo_resposta = 'binaria'"
        questoes = spark.read \
            .format("jdbc") \
            .option("driver", "org.postgresql.Driver") \
            .option("url", "jdbc:postgresql://localhost:5432/previsao-patologias") \
            .option("dbtable", f"({query}) as questoes") \
            .option("user", "postgres") \
            .option("password", "test") \
            .load()
        
        # Trata nome das colunas a serem ignoradas (binárias) transformando-as para o formato snake_case
        questoes_binarias = []
        for c in [row["texto"] for row in questoes.collect()]:
            nome_coluna_tratado = c.replace(" ", "_").replace(".", "").replace("?", "").lower()
            questoes_binarias.append(nome_coluna_tratado)
                    
        # Converta o esquema do DataFrame
        df = spark.read.parquet("./app/storage/parquet/dataframe_modelo.parquet")
        df_sample = df.sample(withReplacement=False, fraction=0.15, seed=42)
        df_sample = df_sample.toPandas().fillna(0).drop(columns=['id_paciente'])
        
        colunas_dummies = [col for col in df_sample.columns if col not in ['id_paciente', 'sexo', 'idade', 'patologia'] + questoes_binarias]
        df_dummies = pd.get_dummies(df_sample, columns=colunas_dummies, dtype=int)
        
        # df_sample.to_csv('./app/storage/csv/dataframe_amostra0.2.csv', index=False)
        df_dummies.to_pickle('./app/storage/pickle/dataframe_amostra_dummies0.15.pkl')
        