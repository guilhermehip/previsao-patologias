from django.core.management.base import BaseCommand, CommandError
from app.models import Patologia
from app.models import CondicaoSaude
from app.models import PatologiaCondicaoSaude
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
                cod_icd_10 = valor.get('icd10-id', {}).upper()
                sintomas = list(valor.get("symptoms", {}).keys())
                antecedentes = list(valor.get("antecedents", {}).keys())
                
                for sintoma in sintomas:
                    patologia = Patologia.objects.get(cod_icd_10 = cod_icd_10)
                    condicaoSintoma = CondicaoSaude.objects.get(slug = sintoma.replace(' ', '_').lower())
                                        
                    patologiaCondicaoSintoma  = PatologiaCondicaoSaude(
                        cod_icd_10=patologia,
                        id_condicao_saude=condicaoSintoma,
                    )
                
                    patologiaCondicaoSintoma.save()
                    
                for antecedente in antecedentes:
                    patologia = Patologia.objects.get(cod_icd_10 = cod_icd_10)
                    condicaoAntecedente = CondicaoSaude.objects.get(slug = antecedente.replace(' ', '_').lower())
                    
                    patologiaCondicaoAntecedente = PatologiaCondicaoSaude(
                        cod_icd_10=patologia,
                        id_condicao_saude=condicaoAntecedente,
                    )
                
                    patologiaCondicaoAntecedente.save()
                
                
