# Generated by Django 3.1.2 on 2020-11-07 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretaria', '0007_alumno_es_egresado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='calif_anual',
            field=models.CharField(blank=True, max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='dni',
            field=models.CharField(max_length=8, unique=True),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='trayectoria',
            field=models.CharField(blank=True, max_length=200, unique=True),
        ),
    ]
