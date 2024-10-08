# Generated by Django 5.1 on 2024-09-05 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0015_proyecto_poste_proyecto'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='contacto',
            field=models.IntegerField(max_length=15, null=True, verbose_name='Telefono'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='mail',
            field=models.CharField(max_length=100, null=True, verbose_name='Correo'),
        ),
    ]
