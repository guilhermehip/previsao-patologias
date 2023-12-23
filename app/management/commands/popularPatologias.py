from django.core.management.base import BaseCommand, CommandError
from app.models import Patologia
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = './app/storage/json'
        
        # Abre o arquivo JSON em modo de leitura
        with open(path+'/release_conditions.json', 'r') as arquivo:
            # Carrega o conteúdo do arquivo JSON
            dados_json = json.load(arquivo)

            # Itera sobre as condições no JSON
            for chave, valor in dados_json.items():
                # Extrai os sintomas
                cod_icd_10 = valor.get('icd10-id', {}).upper()
                patologia_nome = valor.get("cond-name-eng", {}).lower()
                severidade = valor.get("severity", {})
                
                patologia = Patologia(
                    cod_icd_10=cod_icd_10,
                    patologia=patologia_nome,
                    severidade=severidade
                )
                
                patologia.save()
                
