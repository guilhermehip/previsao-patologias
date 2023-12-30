from django.core.management.base import BaseCommand
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import ArrayType, StringType
from pyspark.sql.functions import split, udf
from pyspark.accumulators import AccumulatorParam
from itertools import chain
from pyspark.sql.functions import current_timestamp
    
class Command(BaseCommand):
    def handle(self, *args, **options):

        class ListParam(AccumulatorParam):
            def zero(self, v):
                return []
            def addInPlace(self, variable, value):
                variable.append(value)
                return variable
  
        # Crie uma sessão do Spark
        spark = SparkSession.builder.appName("Processar respostas de ficha clínica") \
            .config("spark.jars", "./app/storage/drivers/postgresql-42.7.1.jar") \
            .config("spark.executor.memory", "4g") \
            .getOrCreate()
            
        # Carregue o arquivo CSV de pacientes
        df = spark.read.format("csv").option("header", True).load("./app/storage/csv/release_patients.csv").limit(1000)
        
        # Carregue o arquivo JSON de evidências
        with open("./app/storage/json/release_evidences.json", "r") as arquivo:
            dados_json = json.load(arquivo)
        
        def parse_evidences(evidence_str):
            # Remove colchetes e aspas
            cleaned_str = evidence_str.replace("[", "").replace("]", "").replace("'", "")
            # Divide a string em uma lista com base nas vírgulas
            evidences_list = cleaned_str.split(", ")
            return evidences_list
        
        # Converta o esquema do DataFrame
        parse_evidences_udf = udf(parse_evidences, ArrayType(StringType()))
        df = df.withColumn("EVIDENCES", parse_evidences_udf(df["EVIDENCES"]))
                
        condicoes_saude = spark.read \
            .format("jdbc") \
            .option("driver", "org.postgresql.Driver") \
            .option("url", "jdbc:postgresql://localhost:5432/previsao-patologias") \
            .option("dbtable", "tb_condicoes_saude") \
            .option("user", "postgres") \
            .option("password", "test") \
            .load()
            
        questoes = spark.read \
            .format("jdbc") \
            .option("driver", "org.postgresql.Driver") \
            .option("url", "jdbc:postgresql://localhost:5432/previsao-patologias") \
            .option("dbtable", "tb_questoes") \
            .option("user", "postgres") \
            .option("password", "test") \
            .load()
            
        alternativas = spark.read \
            .format("jdbc") \
            .option("driver", "org.postgresql.Driver") \
            .option("url", "jdbc:postgresql://localhost:5432/previsao-patologias") \
            .option("dbtable", "tb_alternativas") \
            .option("user", "postgres") \
            .option("password", "test") \
            .load()

        condicoes_saude_collected = condicoes_saude.collect()
        questoes_collected = questoes.collect()
        alternativas_collected = alternativas.collect()
        
        respostas_lista = spark.sparkContext.accumulator([], ListParam())

        def process_row(row):
            evidences = row.EVIDENCES
            index = int(row.ID) + 1
            for evidence in evidences:
                if "_@_" in evidence:
                    slug_condicao_saude, alternativa = evidence.split("_@_")                        
                    condicao_saude = [cs.id_condicao_saude for cs in condicoes_saude_collected if cs['slug'] == slug_condicao_saude][0]
                    alternativa_valor = dados_json[slug_condicao_saude]['value_meaning'].get(alternativa, {}).get('en', alternativa)
                else:
                    slug_condicao_saude = evidence.lower().replace(' ', '_')
                    condicao_saude = [cs.id_condicao_saude for cs in condicoes_saude_collected if cs['slug'] == slug_condicao_saude][0]
                    alternativa_valor = "1"
                           
                questao = [q.id_questao for q in questoes_collected if q['id_condicao_saude'] == condicao_saude][0]
                alternativa = [a.id_alternativa for a in alternativas_collected if a['alternativa'] == alternativa_valor and a['id_questao'] == questao][0]
                
                respostas_lista.add([int(alternativa), int(index), int(questao)])
                
        df = df.repartition(1000)
        df.foreach(process_row)
        print(">>> Processamento de dados rodado! <<<")
        
        flat_respostas_lista = list(chain.from_iterable(respostas_lista.value))
        print(">>> Respostas Flatadas <<<")
        
        respostas = spark.createDataFrame(flat_respostas_lista, ["id_alternativa", "id_ficha_clinica", "id_questao"])
        print(">>> Dataframe criado! <<<")
        
        respostas = respostas.withColumn("dt_criacao", current_timestamp())
        respostas = respostas.withColumn("dt_atualizacao", current_timestamp())
        print(">>> Timestamps criadas! <<<")

        respostas = respostas.repartition(1000)
        respostas.write \
            .format("jdbc") \
            .option("driver", "org.postgresql.Driver") \
            .option("url", "jdbc:postgresql://localhost:5432/previsao-patologias") \
            .option("dbtable", "tb_fichas_clinicas_respostas") \
            .option("user", "postgres") \
            .option("password", "test") \
            .mode("append") \
            .save()
