# Generated by Django 5.1 on 2024-10-11 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0021_proyecto_cant_casas_proyecto_cant_departamentos_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diseno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('olt', models.BooleanField(default=False, verbose_name='¿Va OLT?')),
                ('odf', models.BooleanField(default=False, verbose_name='¿Va ODF?')),
                ('hilo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Hilo')),
                ('slot', models.CharField(blank=True, max_length=100, null=True, verbose_name='slot')),
                ('pon', models.CharField(blank=True, max_length=100, null=True, verbose_name='pon')),
                ('nap8', models.IntegerField(blank=True, null=True, verbose_name='Cuantas nap de 8')),
                ('nap16', models.IntegerField(blank=True, null=True, verbose_name='Cuantas nap de 16')),
                ('m1', models.IntegerField(blank=True, null=True, verbose_name='Mufa M1')),
                ('m2', models.IntegerField(blank=True, null=True, verbose_name='Mufa M2')),
                ('odf1', models.IntegerField(blank=True, null=True, verbose_name='odf puertos:')),
                ('odf2', models.IntegerField(blank=True, null=True, verbose_name='odf puertos:')),
                ('odf3', models.IntegerField(blank=True, null=True, verbose_name='odf puertos:')),
                ('hp', models.IntegerField(blank=True, null=True, verbose_name='HP')),
                ('proveedor', models.ManyToManyField(blank=True, to='erp.proveedor', verbose_name='Proveedores')),
            ],
        ),
    ]
