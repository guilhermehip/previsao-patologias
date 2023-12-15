from django.core.management.base import BaseCommand, CommandError
from app.models import Paciente
from os import listdir
from os.path import isfile, join
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **options):
        path = './app/storage/csv'
        csv_files = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
        
        df_concat = pd.concat([pd.read_csv(f) for f in csv_files], ignore_index=True)
        
        df_concat.to_csv(path+'/release_patients.csv', index_label='ID')
