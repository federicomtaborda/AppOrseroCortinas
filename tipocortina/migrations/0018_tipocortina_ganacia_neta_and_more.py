# Generated by Django 5.1.6 on 2025-03-02 04:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipocortina', '0017_tipocortina_costo_mano_obra_tipocortina_costo_total_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipocortina',
            name='ganacia_neta',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Gancia Neta'),
        ),
        migrations.AddField(
            model_name='tipocortina',
            name='ganacia_porcentaje',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='% Ganancia'),
        ),
    ]
