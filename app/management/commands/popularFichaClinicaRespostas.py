from django.core.management.base import BaseCommand
from app.models import Alternativa, CondicaoSaude, Questao, FichaClinica, FichaClinicaRespostas
import pandas as pd
import ast
import json

class Command(BaseCommand):
    def handle(self, *args, **options):
        pacientes_csv = './app/storage/csv/release_patients.csv'
        df = pd.read_csv(pacientes_csv)

        json_path = './app/storage/json'
        with open(json_path + '/release_evidences.json', 'r') as arquivo:
            dados_json = json.load(arquivo)

        ficha_clinica_respostas_list = []

        for index, row in df.iterrows():
            # Convert the string representation of the list to an actual list
            evidences_array = ast.literal_eval(row["EVIDENCES"])

            id_ficha_clinica = row['ID'] + 1
            ficha_clinica = FichaClinica.objects.get(id_ficha_clinica=id_ficha_clinica)

            for element in evidences_array:
                if "_@_" in element:
                    [slug_condicao_saude, alternativa] = element.split("_@_")
                    condicao_saude = CondicaoSaude.objects.get(slug=slug_condicao_saude)
                    en_value = dados_json[slug_condicao_saude]['value_meaning'].get(alternativa, {}).get('en',
                                                                                                             alternativa)

                    questao = Questao.objects.get(id_condicao_saude=condicao_saude)
                    alternativa = Alternativa.objects.get(alternativa=en_value, id_questao=questao)

                    resposta = FichaClinicaRespostas(
                        id_ficha_clinica=ficha_clinica,
                        id_questao=questao,
                        id_alternativa=alternativa,
                    )

                    ficha_clinica_respostas_list.append(resposta)

                else:
                    condicao_saude = CondicaoSaude.objects.get(slug=element.lower().replace(' ', '_').lower())
                    questao = Questao.objects.get(id_condicao_saude=condicao_saude)
                    alternativa = Alternativa.objects.get(alternativa="1", id_questao=questao)

                    resposta = FichaClinicaRespostas(
                        id_ficha_clinica=ficha_clinica,
                        id_questao=questao,
                        id_alternativa=alternativa,
                    )

                    ficha_clinica_respostas_list.append(resposta)

        # Use bulk_create para inserir várias instâncias de uma vez
        FichaClinicaRespostas.objects.bulk_create(ficha_clinica_respostas_list)
