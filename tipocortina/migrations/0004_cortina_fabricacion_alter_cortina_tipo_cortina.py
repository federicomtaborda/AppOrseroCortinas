# Generated by Django 5.1.6 on 2025-03-24 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipocortina', '0003_rename_tiptubo_tipotubo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cortina',
            name='fabricacion',
            field=models.BooleanField(default=False, verbose_name='Fabricación Propia'),
        ),
        migrations.AlterField(
            model_name='cortina',
            name='tipo_cortina',
            field=models.BooleanField(default=False, verbose_name='Cortina de Confección'),
        ),
    ]
