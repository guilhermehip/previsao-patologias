from django.core.management.base import BaseCommand
from app.models import Questao, Alternativa
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        path = './app/storage/json'
        
        # Abre o arquivo JSON em modo de leitura
        with open(path+'/release_evidences.json', 'r') as arquivo:
            # Carrega o conteúdo do arquivo JSON
            dados_json = json.load(arquivo)

            # Lista para armazenar as instâncias a serem criadas
            alternativas = []

            # Itera sobre as condições no JSON
            for chave, valor in dados_json.items():
                # Extrai os sintomas
                texto = valor.get('question_en', {}).upper()
                
                # Se for vazio, registra os valores 0 e 1
                questao = Questao.objects.get(texto=texto)
                if questao.tipo_resposta == 'multiescolha':
                    value_meaning = valor.get('value_meaning', {})
                    for sub_chave, sub_valor in value_meaning.items():
                        en_value = sub_valor.get('en', '')
                        # Adiciona instância à lista
                        alternativas.append(Alternativa(id_questao=questao, alternativa=en_value))
                elif questao.tipo_resposta == 'categorica':
                    value_meaning = valor.get('value_meaning', {})
                    if not value_meaning:
                        alternativas.append(Alternativa(id_questao=questao, alternativa=0))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=1))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=2))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=3))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=4))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=5))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=6))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=7))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=8))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=9))
                        alternativas.append(Alternativa(id_questao=questao, alternativa=10))
                    else: 
                        for sub_chave, sub_valor in value_meaning.items():
                            en_value = sub_valor.get('en', '')
                            # Adiciona instância à lista
                            alternativas.append(Alternativa(id_questao=questao, alternativa=en_value))
                else:
                    alternativas.append(Alternativa(id_questao=questao, alternativa=0))
                    alternativas.append(Alternativa(id_questao=questao, alternativa=1))
                
            Alternativa.objects.bulk_create(alternativas)
