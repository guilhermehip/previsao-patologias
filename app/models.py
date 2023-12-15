from django.db import models

class Paciente(models.Model):
    class Meta:
      db_table = "tb_pacientes"
        
    SEXO = {
      "M": "Masculino",
      "F": "Feminino",
    }
  
    id_paciente = models.AutoField(primary_key=True)
    idade = models.IntegerField()
    sexo = models.CharField(max_length=1, choices={i: i for i in SEXO})
    dt_criacao = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)
    dt_atualizacao = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
