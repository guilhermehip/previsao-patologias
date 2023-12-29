from django.db import models
from django.apps import apps
from app.models import Paciente

class FichaClinica(models.Model):
    class Meta:
        db_table = "tb_fichas_clinicas"
        
    id_ficha_clinica = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, db_column='id_paciente')
    dt_criacao = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    dt_atualizacao = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)