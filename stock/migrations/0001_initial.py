# Generated by Django 5.1.6 on 2025-03-24 08:42

import datetime
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metros_cuadrados', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='M² Tela ')),
                ('cadena', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Cadena')),
                ('zocalo', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Zocalo')),
                ('tapa_zocalo', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tapa Zocalo')),
                ('peso_cadena', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Peso Cadena')),
                ('tope', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tope')),
                ('union', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Unión')),
                ('tipo_stock', models.CharField(blank=True, choices=[('Ingreso', 'Ingreso de Stock'), ('Egreso', 'Egreso de Stock')], max_length=30, null=True, verbose_name='Tipo de Stock')),
                ('fecha_stock', models.DateField(default=datetime.date.today, verbose_name='Fecha Stock')),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_articulo', to='tipocortina.cortina')),
            ],
            options={
                'verbose_name': 'Stock',
                'verbose_name_plural': 'Stocks',
            },
        ),
    ]
