# Generated by Django 5.1.6 on 2025-03-27 08:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tipocortina', '0005_cortina_costo_m2'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipocortina',
            name='ancho_tubo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Ancho Tubo (mts)'),
        ),
        migrations.AlterField(
            model_name='tipocortina',
            name='cadena',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='valor calculado automáticamente', max_digits=6, null=True, verbose_name='Cadena'),
        ),
        migrations.AlterField(
            model_name='tipocortina',
            name='cantidad',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='tipocortina',
            name='zocalo',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, help_text='valor calculado automáticamente', max_digits=6, null=True, verbose_name='Zocalo (mts)'),
        ),
    ]
