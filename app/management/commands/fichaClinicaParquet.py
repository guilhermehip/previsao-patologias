from django.core.management.base import BaseCommand
from pyspark.sql import SparkSession
    
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Crie uma sessão do Spark
        spark = SparkSession.builder.appName("Gravar respostas de ficha clínica em formato Parquet") \
            .config("spark.jars", "./app/storage/drivers/postgresql-42.7.1.jar") \
            .getOrCreate()
        
        # Converta o esquema do DataFrame
        df = spark.read.option("header",True).csv("./app/storage/csv/ficha_clinica_estruturada.csv")
        df = df.repartition(100)
        
        df.write \
            .format("parquet") \
            .mode("overwrite") \
            .option("path", './app/storage/parquet/ficha_clinica_estruturada.parquet') \
            .save()