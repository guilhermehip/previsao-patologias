from django.db import models

class CondicaoSaude(models.Model):
    class Meta:
      db_table = "tb_condicoes_saude"
  
    TIPOS = {
      "sintoma": "sintoma",
      "antecedente": "antecedente",
    }
        
    id_condicao_saude = models.AutoField(primary_key=True)
    slug = models.CharField()
    tipo = models.CharField(choices={i: i for i in TIPOS})
    dt_criacao = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    dt_atualizacao = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
