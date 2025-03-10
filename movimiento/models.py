import datetime

from django.core.validators import MinValueValidator
from django.db import models

from cliente.models import Cliente
from ordendetrabajo.models import OrdenTrabajo


class TipoMovimiento(models.Model):
    nombre = models.CharField(max_length=100)
    egreso = models.BooleanField(verbose_name='Egreso de Dinero', default=False)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(TipoMovimiento, self).save(*args, **kwargs)


class Movimiento(models.Model):
    numero_mov = models.BigIntegerField(
        unique=True,
        editable=False,
    )

    tipo_movimiento = models.ForeignKey(
        TipoMovimiento,
        on_delete=models.CASCADE,
        verbose_name='Tipo Movimiento'
    )

    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='monto',
        validators=[MinValueValidator(0)]
    )

    detalle = models.TextField(
        blank=True,
        null=True,
        verbose_name='Detalle'
    )

    fecha = models.DateField(
        default=datetime.date.today,
        verbose_name='Fecha Mov'
    )

    def save(self, *args, **kwargs):
        if not self.numero_mov:
            ultimo = Movimiento.objects.all().order_by('-numero_mov').first()
            self.numero_mov = (ultimo.numero_mov + 1) if ultimo else 1

        # hacer monto negativo si tipo egreso es True
        if self.monto != 0 and self.tipo_movimiento.egreso:
            self.monto = self.monto * -1
        super().save(*args, **kwargs)

    @property
    def numero_movimiento(self):
        return f"MOV-{str(self.numero_mov).zfill(8)}"

    def __str__(self):
        return self.numero_movimiento
