from django.core.management.base import BaseCommand, CommandError
from app.models import Questao
from app.models import CondicaoSaude
import json


class Command(BaseCommand):
    def handle(self, *args, **options):
        path = './app/storage/json'
        
        # Abre o arquivo JSON em modo de leitura
        with open(path+'/release_evidences.json', 'r') as arquivo:
            # Carrega o conteúdo do arquivo JSON
            dados_json = json.load(arquivo)

            # Itera sobre as condições no JSON
            for chave, valor in dados_json.items():
              slug_questao_mae = valor.get('code_question', {}).replace(', ', '_').replace(' ', '_').strip().lower()
              condicao_saude_mae = CondicaoSaude.objects.get(slug=slug_questao_mae)
              
              questao_mae = Questao.objects.get(id_condicao_saude = condicao_saude_mae)
              
              if(chave.lower() != slug_questao_mae):
                  condicao_saude = CondicaoSaude.objects.get(slug=chave.lower())
                  Questao.objects.filter(id_condicao_saude=condicao_saude).update(id_questao_mae=questao_mae)
                  
