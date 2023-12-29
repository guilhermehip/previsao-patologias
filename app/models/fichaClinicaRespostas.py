from django.db import models
from django.apps import apps
from app.models import Questao, FichaClinica, Alternativa

class FichaClinicaRespostas(models.Model):
    class Meta:
        db_table = "tb_fichas_clinicas_respostas"
        
    id_ficha_clinica_resposta = models.AutoField(primary_key=True)
    id_ficha_clinica = models.ForeignKey(FichaClinica, on_delete=models.CASCADE, db_column='id_ficha_clinica')
    id_questao = models.ForeignKey(Questao, on_delete=models.CASCADE, db_column='id_questao')
    id_alternativa = models.ForeignKey(Alternativa, on_delete=models.CASCADE, db_column='id_alternativa')
    dt_criacao = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    dt_atualizacao = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)