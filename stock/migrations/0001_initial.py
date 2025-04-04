# Generated by Django 5.1.6 on 2025-03-25 19:34

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StockCortinas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('articulo', models.CharField(max_length=180, null=True, verbose_name='Cortina Descripción')),
                ('metros_cuadrados', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=6, null=True, verbose_name='M² Tela ')),
                ('tipo_stock_cotinas', models.CharField(choices=[('Ingreso', 'Ingreso de Stock'), ('Egreso', 'Egreso de Stock')], max_length=30, null=True, verbose_name='Tipo de Stock Cotinas')),
                ('fecha_stock_cortinas', models.DateField(default=datetime.date.today, verbose_name='Fecha Stock Cortina')),
                ('estado_stock_cortinas', models.CharField(choices=[('Ingreso', 'Comprometido'), ('Egreso', 'Aplicado')], max_length=30, null=True, verbose_name='Estado Stock')),
            ],
            options={
                'verbose_name': 'Stock Cortinas',
                'verbose_name_plural': 'Stocks Cortinas',
            },
        ),
        migrations.CreateModel(
            name='StockInsumos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cadena', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Cadena')),
                ('zocalo', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6, null=True, verbose_name='Zocalo')),
                ('tapa_zocalo', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tapa Zocalo')),
                ('peso_cadena', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Peso Cadena')),
                ('tope', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Tope')),
                ('union', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Unión')),
                ('tipo_stock_insumos', models.CharField(choices=[('Ingreso', 'Ingreso de Stock'), ('Egreso', 'Egreso de Stock')], max_length=30, null=True, verbose_name='Tipo de Stock Insumos')),
                ('fecha_stock_insumos', models.DateField(default=datetime.date.today, verbose_name='Fecha Stock Insumo')),
                ('estado_stock_insumos', models.CharField(choices=[('Ingreso', 'Comprometido'), ('Egreso', 'Aplicado')], max_length=30, null=True, verbose_name='Estado Stock')),
            ],
            options={
                'verbose_name': 'Stock Insumos',
                'verbose_name_plural': 'Stocks Insumos',
            },
        ),
    ]
