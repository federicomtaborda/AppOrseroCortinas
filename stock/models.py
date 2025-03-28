import datetime

from django.core.validators import MinValueValidator
from django.db import models

from configuracion.opciones import TIPO_STOCK, ESTADO_STOCK


class StockCortinas(models.Model):

    articulo = models.CharField(
        max_length=180,
        verbose_name='Cortina Descripción',
        null=True,
    )

    metros_cuadrados = models.DecimalField(
        verbose_name='M² Tela ',
        default=0,
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
    )

    tipo_stock_cortinas = models.CharField(
        max_length=30,
        verbose_name='Tipo de Stock Cotinas',
        null=True,
        choices=TIPO_STOCK,
    )

    fecha_stock_cortinas = models.DateField(
        default=datetime.date.today,
        verbose_name='Fecha Stock Cortina'
    )

    estado_stock_cortinas = models.CharField(
        max_length=30,
        verbose_name='Estado Stock',
        null=True,
        choices=ESTADO_STOCK,
    )

    class Meta:
        verbose_name = 'Stock Cortinas'
        verbose_name_plural = 'Stocks Cortinas'

    def __str__(self):
        return f"{self.articulo} - {self.metros_cuadrados} m²"


class StockInsumos(models.Model):

    cadena = models.DecimalField(
        verbose_name='Cadena',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        default=0.00
    )

    zocalo = models.DecimalField(
        verbose_name='Zocalo',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        default=0.00
    )

    tapa_zocalo = models.IntegerField(
        verbose_name='Tapa Zocalo',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        default=0
    )

    peso_cadena = models.IntegerField(
        verbose_name='Peso Cadena',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        default=0
    )

    tope = models.IntegerField(
        verbose_name='Tope',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        default=0
    )

    union = models.IntegerField(
        verbose_name='Unión',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        default=0
    )

    tipo_stock_insumos = models.CharField(
        max_length=30,
        verbose_name='Tipo de Stock Insumos',
        null=True,
        choices=TIPO_STOCK,
    )

    fecha_stock_insumos = models.DateField(
        default=datetime.date.today,
        verbose_name='Fecha Stock Insumo'
    )

    estado_stock_insumos = models.CharField(
        max_length=30,
        verbose_name='Estado Stock',
        null=True,
        choices=ESTADO_STOCK,
    )

    class Meta:
        verbose_name = 'Stock Insumos'
        verbose_name_plural = 'Stocks Insumos'

    def __str__(self):
        return ''