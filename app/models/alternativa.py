from django.db import models
from django.apps import apps
from app.models import Questao

class Alternativa(models.Model):
    class Meta:
        db_table = "tb_alternativas"
        
    id_alternativa = models.AutoField(primary_key=True)
    id_questao = models.ForeignKey(Questao, on_delete=models.CASCADE, db_column='id_questao')
    alternativa = models.TextField()
