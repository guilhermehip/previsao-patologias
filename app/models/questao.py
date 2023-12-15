from django.db import models

class Questao(models.Model):
    class Meta:
        db_table = "tb_questoes"
        
    TIPO_RESPOSTA = {
      "binaria": "Binaria",
      "categorica": "Categorica",
    }
  
    id_questao = models.AutoField(primary_key=True)
    id_questao_mae = models.ForeignKey(
        "self",  # "self" indica que é uma chave estrangeira para o mesmo modelo
        on_delete=models.CASCADE,
        null=True,  # Permite nulos para a primeira instância
        blank=True,  # Permite campos em branco para a primeira instância
    )
    slug = models.CharField()
    texto = models.TextField()
    validador = models.JSONField()
    tipo_resposta = models.CharField(choices={i: i for i in TIPO_RESPOSTA})
    resposta_padrao = models.CharField()
    antecedente = models.BooleanField()
    dt_criacao = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    dt_atualizacao = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
