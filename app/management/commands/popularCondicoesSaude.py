from django.core.management.base import BaseCommand, CommandError
from app.models import CondicaoSaude
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = './app/storage/json'
        
        # Abre o arquivo JSON em modo de leitura
        with open(path+'/release_conditions.json', 'r') as arquivo:
            # Carrega o conteúdo do arquivo JSON
            dados_json = json.load(arquivo)
            sintomas = []
            antecedentes = []

            # Itera sobre as condições no JSON
            for chave, valor in dados_json.items():
                # Extrai os sintomas
                sintomas_condicao = valor.get("symptoms", {}).keys()
                sintomas.extend(sintomas_condicao)

                # Extrai os antecedentes
                antecedentes_condicao = valor.get("antecedents", {}).keys()
                antecedentes.extend(antecedentes_condicao)

            # Remove duplicatas, se houver
            sintomas = list(set(sintomas))
            antecedentes = list(set(antecedentes))

            for sintoma in sintomas:
                slug_sintoma = sintoma.replace(' ', '_').lower()
                CondicaoSaude.objects.get_or_create(slug=slug_sintoma, tipo='sintoma')
                
            for antecedente in antecedentes:
                slug_antecedente = antecedente.replace(' ', '_').lower()
                CondicaoSaude.objects.get_or_create(slug=slug_antecedente, tipo='antecedente')
