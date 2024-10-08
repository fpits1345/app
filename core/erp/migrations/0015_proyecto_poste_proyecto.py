# Generated by Django 5.1 on 2024-09-05 13:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0014_remove_poste_proyecto_delete_proyecto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Nombre')),
                ('desc', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
            ],
        ),
        migrations.AddField(
            model_name='poste',
            name='proyecto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.proyecto', verbose_name='Proyecto'),
        ),
    ]
