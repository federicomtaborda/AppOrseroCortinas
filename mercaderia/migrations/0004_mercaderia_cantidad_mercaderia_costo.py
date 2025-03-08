# Generated by Django 5.1.6 on 2025-03-04 14:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mercaderia', '0003_rename_fecha_creacion_mercaderia_fecha_ingreso'),
    ]

    operations = [
        migrations.AddField(
            model_name='mercaderia',
            name='cantidad',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Cantidad Unid.'),
        ),
        migrations.AddField(
            model_name='mercaderia',
            name='costo',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='costo'),
        ),
    ]
