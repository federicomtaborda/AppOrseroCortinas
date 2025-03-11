import datetime

from django.core.validators import MinValueValidator
from django.db import models

from tipocortina.models import Cortina


class Mercaderia(models.Model):

    articulo = models.ForeignKey(
        Cortina,
        on_delete=models.CASCADE,
        related_name='mercaderia'
    )

    metros_cuadrados = models.DecimalField(
        verbose_name='Metros²',
        max_digits=20,
        validators=[MinValueValidator(0)],
        decimal_places=2,
        default=0
    )

    cantidad = models.IntegerField(
        verbose_name='Cantidad Unid.',
        validators=[MinValueValidator(0)],
        default=0
    )

    costo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='costo',
        default=0,
        validators=[MinValueValidator(0)]
    )

    fecha_ingreso = models.DateField(
        default=datetime.date.today,
        verbose_name='Fecha Ingreso'
    )

    observaciones = models.TextField(
        verbose_name='Observaciones',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Mercaderia'
        verbose_name_plural = 'Mercaderia'

    def __str__(self):
        return self.articulo.nombre
