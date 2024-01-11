from django.core.management.base import BaseCommand
from app.models import Patologia, FichaClinica, Diagnostico, CondicaoSaude
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
        
        df = pd.read_csv(pacientes_csv, usecols=['PATHOLOGY', 'INITIAL_EVIDENCE'])
        
        for index, row in df.iterrows():
            print(index)
            for chave, valor in dados_json.items():
                # Extrai os sintomas
                patologia_nome = valor.get("cond-name-fr", {}).lower()
                patologia_ficha_str  = row['PATHOLOGY'].lower()

                if patologia_ficha_str == patologia_nome:
                    cod_icd_10 = valor.get("icd10-id", {}).upper()
                    patologia = Patologia.objects.get(cod_icd_10=cod_icd_10)
                    ficha_clinica = FichaClinica.objects.get(id_ficha_clinica=index+1)
                    evidencia_inicial = row['INITIAL_EVIDENCE'].replace(' ', '_').lower()           
                    condicao_saude = CondicaoSaude.objects.get(slug=evidencia_inicial)
                                        
                    diagnostico = Diagnostico(
                        id_ficha_clinica=ficha_clinica,
                        cod_icd_10=patologia,
                        evidencia_inicial=condicao_saude
                    )
                    
                    diagnostico.save()
