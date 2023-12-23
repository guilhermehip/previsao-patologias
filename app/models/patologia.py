from django.db import models

class Patologia(models.Model):
    class Meta:
      db_table = "tb_patologias"
  
    cod_icd_10 = models.CharField(primary_key=True, unique=True)
    patologia = models.CharField()
    severidade = models.IntegerField(choices=((i,i) for i in range(1, 5)))
    dt_criacao = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    dt_atualizacao = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
