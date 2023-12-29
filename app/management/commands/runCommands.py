from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.core.management import call_command

class Command(BaseCommand):
    def handle(self, *args, **options):
        scripts = [
            'popularPacientes',
            'popularPatologias',
            'popularCondicoesSaude',
            'popularPatologiasCondicoes',
            'popularQuestoes',
            'popularQuestoesFk',
            'popularAlternativas',
            'popularFichaClinica',
            'popularFichaClinicaRespostas'
        ]

        for script in scripts:
            call_command(script)
            print(f'Script {script} rodado!')