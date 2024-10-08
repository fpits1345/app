# Generated by Django 5.1 on 2024-10-07 13:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0018_alter_proyecto_contacto_alter_proyecto_direccion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Nombre')),
            ],
        ),
        migrations.AddField(
            model_name='proyecto',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='erp.proveedor', verbose_name='Proyecto'),
        ),
    ]
