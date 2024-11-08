# Generated by Django 5.1 on 2024-10-24 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erp', '0029_remove_proyecto_desc_proyecto_adm_alter_diseno_m1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='diseno',
            name='cable12',
            field=models.IntegerField(blank=True, null=True, verbose_name='Metros de cable 12'),
        ),
        migrations.AddField(
            model_name='diseno',
            name='cable24',
            field=models.IntegerField(blank=True, null=True, verbose_name='Metros de cable 24'),
        ),
        migrations.AddField(
            model_name='diseno',
            name='cable4',
            field=models.IntegerField(blank=True, null=True, verbose_name='metros de cable 4'),
        ),
        migrations.AddField(
            model_name='diseno',
            name='cable48',
            field=models.IntegerField(blank=True, null=True, verbose_name='Metros de cable 48'),
        ),
        migrations.AddField(
            model_name='diseno',
            name='cable8',
            field=models.IntegerField(blank=True, null=True, verbose_name='metros de cable 8'),
        ),
        migrations.AddField(
            model_name='diseno',
            name='cable96',
            field=models.IntegerField(blank=True, null=True, verbose_name='Metros de cable 96'),
        ),
    ]
