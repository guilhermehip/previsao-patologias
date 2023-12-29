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
                # Extrai os sintomas
                id_condicao_saude = CondicaoSaude.objects.get(slug = chave.lower())
                texto = valor.get('question_en', {}).upper()
                resposta_padrao = valor.get('default_value', {})
                
                tipo_dado = valor.get('data_type', {}).upper()
                if tipo_dado == 'B':
                  tipo_resposta = 'binaria'
                elif tipo_dado == 'C':
                  tipo_resposta = 'categorica'
                else:
                  tipo_resposta = 'multiescolha'
                
                questao = Questao(
                    id_condicao_saude=id_condicao_saude,
                    texto=texto,
                    resposta_padrao=resposta_padrao,
                    tipo_resposta=tipo_resposta
                )
                
                questao.save()


                
