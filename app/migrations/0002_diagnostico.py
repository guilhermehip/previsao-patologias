# Generated by Django 5.0 on 2024-01-03 02:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnostico',
            fields=[
                ('id_diagnostico', models.AutoField(primary_key=True, serialize=False)),
                ('id_ficha_clinica', models.ForeignKey(db_column='id_ficha_clinica', on_delete=django.db.models.deletion.CASCADE, to='app.fichaclinica')),
                ('cod_icd_10', models.ForeignKey(db_column='cod_icd_10', on_delete=django.db.models.deletion.CASCADE, to='app.patologia')),
                ('dt_criacao', models.DateTimeField(auto_now_add=True, null=True)),
                ('dt_atualizacao', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'db_table': 'tb_diagnosticos',
            },
        ),
    ]
