from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from app.models import Paciente
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        pacientes_csv = './app/storage/csv/release_patients.csv'
        
        ## Idade, Sexo
        df_chunks = pd.read_csv(pacientes_csv, chunksize=10000)
        
        for chunk in df_chunks:
          # Processar cada chunk
          df = chunk[['AGE', 'SEX']]
          pacientes = [Paciente(idade=row['AGE'], sexo=row['SEX']) for index, row in df.iterrows()]

          with transaction.atomic():
            Paciente.objects.bulk_create(pacientes)
