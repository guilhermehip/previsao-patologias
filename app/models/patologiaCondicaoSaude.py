from django.db import models
from app.models import Patologia
from app.models import CondicaoSaude

class PatologiaCondicaoSaude(models.Model):
    class Meta:
      db_table = "tb_patologia_condicao"
        
    cod_icd_10 = models.ForeignKey(Patologia, on_delete=models.CASCADE, db_column='cod_icd_10')
    id_condicao_saude = models.ForeignKey(CondicaoSaude, on_delete=models.CASCADE, db_column='id_condicao_saude')
