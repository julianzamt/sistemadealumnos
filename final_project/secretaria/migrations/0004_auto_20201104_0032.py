# Generated by Django 3.1.2 on 2020-11-04 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secretaria', '0003_auto_20201102_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alumno',
            name='calif_anual',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='dni',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='alumno',
            name='trayectoria',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
