from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from app.models import Patologia, FichaClinica, Diagnostico
import pandas as pd
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        pacientes_csv = './app/storage/csv/release_patients.csv'
        json_path = './app/storage/json'
        
        # Abre o arquivo JSON em modo de leitura
        with open(json_path+'/release_conditions.json', 'r') as arquivo:
            # Carrega o conteúdo do arquivo JSON
            dados_json = json.load(arquivo)
        
        df = pd.read_csv(pacientes_csv, usecols=['PATHOLOGY'])
        
        diagnostico_objects = []
        for index, patologia_ficha in df.iterrows():
            print(index)
            for chave, valor in dados_json.items():
                # Extrai os sintomas
                patologia_nome = valor.get("cond-name-fr", {}).lower()
                patologia_ficha_str  = patologia_ficha['PATHOLOGY'].lower()

                if patologia_ficha_str == patologia_nome:
                    cod_icd_10 = valor.get("icd10-id", {}).upper()
                    patologia = Patologia.objects.get(cod_icd_10=cod_icd_10)
                    ficha_clinica = FichaClinica.objects.get(id_ficha_clinica=index+1)
                    
                    diagnostico_objects.append(Diagnostico(id_ficha_clinica=ficha_clinica, cod_icd_10=patologia))
                    
        Diagnostico.objects.bulk_create(diagnostico_objects)
