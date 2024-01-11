from django.db import models
from app.models import Patologia, FichaClinica, CondicaoSaude

class Diagnostico(models.Model):
    class Meta:
        db_table = "tb_diagnosticos"
        
    id_diagnostico = models.AutoField(primary_key=True)
    id_ficha_clinica = models.ForeignKey(FichaClinica, on_delete=models.CASCADE, db_column='id_ficha_clinica')
    cod_icd_10 = models.ForeignKey(Patologia, on_delete=models.CASCADE, db_column='cod_icd_10')
    evidencia_inicial = models.ForeignKey(CondicaoSaude, on_delete=models.CASCADE, db_column='evidencia_inicial')
    dt_criacao = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    dt_atualizacao = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
