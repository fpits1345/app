# Generated by Django 5.1 on 2024-10-14 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0026_diseno_obs_alter_diseno_hp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diseno',
            name='odf',
            field=models.IntegerField(default=False, verbose_name='ODF'),
        ),
        migrations.AlterField(
            model_name='diseno',
            name='odf1',
            field=models.IntegerField(blank=True, null=True, verbose_name='odf puertos'),
        ),
        migrations.AlterField(
            model_name='diseno',
            name='odf2',
            field=models.IntegerField(blank=True, null=True, verbose_name='odf puertos'),
        ),
        migrations.AlterField(
            model_name='diseno',
            name='odf3',
            field=models.IntegerField(blank=True, null=True, verbose_name='odf puertos'),
        ),
        migrations.AlterField(
            model_name='diseno',
            name='olt',
            field=models.IntegerField(default=False, verbose_name='OLT'),
        ),
    ]
