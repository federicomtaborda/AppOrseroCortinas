import datetime

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from cliente.models import Cliente, Colocador


class EstadoOrden:
    PENDIENTE = 'pendiente'
    DEMORADA = 'demorada'
    TERMINADA = 'terminada'


class TipoOrden:
    PRESUPUESTO = 'PRESUPUESTO'
    VENTA = 'VENTA'


TIPO_ORDEN = (
    (TipoOrden.PRESUPUESTO, "PRESUPUESTO"),
    (TipoOrden.VENTA, "VENTA"),
)

ESTADO_ORDEN = (
    (EstadoOrden.PENDIENTE, "Pendiente"),
    (EstadoOrden.DEMORADA, "Demorada"),
    (EstadoOrden.TERMINADA, "Terminada"),
)


class OrdenTrabajo(models.Model):
    contador = models.BigIntegerField(
        unique=True,
        editable=False,
    )

    tipo_orden = models.CharField(
        max_length=50,
        choices=TIPO_ORDEN,
        default=TipoOrden.PRESUPUESTO,
        verbose_name='Tipo de Orden',
    )

    fecha_creacion = models.DateField(
        default=datetime.date.today,
        verbose_name='Fecha de Orden'
    )

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        verbose_name='Cliente',
        null=True,
        blank=True,
    )

    colocador = models.ForeignKey(
        Colocador,
        on_delete=models.PROTECT,
        verbose_name='Colocador',
        null=True,
        blank=True,
    )

    observaciones = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción'
    )

    estado_orden = models.CharField(
        max_length=50,
        choices=ESTADO_ORDEN,
        default=EstadoOrden.PENDIENTE,
        verbose_name='Estado de Orden'
    )

    tiempo_entrega = models.DateField(
        verbose_name='Tiempo de Entrega',
        null=True,
        blank=True,
    )

    metros_totales = models.IntegerField(
        verbose_name='Metros² Totales',
        validators=[MinValueValidator(0)],
        default=0
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='total',
        default=0,
        validators=[MinValueValidator(0)]
    )

    prioridad = models.BooleanField(
        verbose_name='Orden Prioritaria',
        default=False
    )

    class Meta:
        verbose_name = 'Orden de Trabajo'
        verbose_name_plural = 'Órdenes de Trabajo'
        ordering = ['contador']

    def save(self, *args, **kwargs):
        if not self.contador:
            # Obtener el último contador y sumar 1
            ultimo = OrdenTrabajo.objects.all().order_by('-contador').first()
            self.contador = (ultimo.contador + 1) if ultimo else 1
        super().save(*args, **kwargs)

    @property
    def numero_orden(self):
        return f"ORDEN-{str(self.contador).zfill(8)}"

    def __str__(self):
        return self.numero_orden


@receiver(pre_save, sender=OrdenTrabajo)
def actualizar_tipo_orden(sender, instance, **kwargs):
    if instance.estado_orden == EstadoOrden.TERMINADA:
        instance.tipo_orden = TipoOrden.VENTA
