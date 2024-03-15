from django.core.management.base import BaseCommand
from pyspark.sql import SparkSession
from imblearn.over_sampling import SMOTE
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
        df_sample = df.sample(withReplacement=False, fraction=0.05, seed=42)
        df_sample = df_sample.toPandas().fillna(0).drop(columns=['id_paciente'])
        
        colunas_dummies = [col for col in df_sample.columns if col not in ['idade', 'patologia', 'severidade'] + questoes_binarias]
        df_dummies = pd.get_dummies(df_sample, columns=colunas_dummies, dtype=int)
        
        X = df_dummies.drop(columns=['patologia'])
        y = df_dummies['patologia']

        smote = SMOTE(sampling_strategy='auto', random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y)

        # Criar um novo DataFrame com a sobreamostra
        df_resampled = pd.concat([pd.DataFrame(X_resampled, columns=X.columns), pd.Series(y_resampled, name='patologia')], axis=1)

        # Salvar a sobreamostra
        df_resampled.to_pickle('./app/storage/pickle/dataframe_smote0.10.pkl')