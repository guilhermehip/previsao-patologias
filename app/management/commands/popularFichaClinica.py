from django.core.management.base import BaseCommand
from app.models import Paciente, FichaClinica
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        pacientes_csv = './app/storage/csv/release_patients.csv'

        # Leitura do CSV
        df_chunks = pd.read_csv(pacientes_csv)

        # Mapeamento dos IDs do DataFrame para instâncias de Paciente
        pacientes_mapping = {row['ID'] + 1: Paciente(id_paciente=row['ID'] + 1) for _, row in df_chunks.iterrows()}

        # Criação das instâncias de FichaClinica associadas aos Pacientes
        fichas_clinicas = [FichaClinica(id_paciente=paciente) for paciente in pacientes_mapping.values()]

        # Salvando as instâncias de FichaClinica
        FichaClinica.objects.bulk_create(fichas_clinicas)
