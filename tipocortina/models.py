from django.core.validators import MinValueValidator
from django.db import models

from ordendetrabajo.models import OrdenTrabajo


class Modelo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Modelo')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Modelo, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre}"


class Cortina(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Cortina')
    codigo = models.CharField(max_length=25, verbose_name='Código', null=True, blank=True)
    modelo = models.ForeignKey(Modelo, verbose_name='Modelo', on_delete=models.PROTECT)
    caracteristicas = models.TextField(verbose_name='Caracteristicas', null=True, blank=True)
    tipo_cortina = models.BooleanField(verbose_name='Cortina de Confección ', default=False)

    class Meta:
        verbose_name = 'Tipo de Cortina'
        verbose_name_plural = 'Tipos de Cortina'

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Cortina, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.modelo}"


class TipoCortina(models.Model):
    articulo = models.ForeignKey(
        Cortina,
        on_delete=models.CASCADE,
        related_name='cortina'
    )

    orden_trabajo = models.ForeignKey(
        OrdenTrabajo,
        verbose_name='Orden Trabajo',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    alto = models.IntegerField(
        verbose_name='Alto (mts)',
        validators=[MinValueValidator(0)],
        default=0
    )

    ancho = models.IntegerField(
        verbose_name='Ancho (mts)',
        validators=[MinValueValidator(0)],
        default=0
    )

    metros_cuadrados = models.IntegerField(
        verbose_name='Metros²',
        validators=[MinValueValidator(0)],
        default=0
    )

    mando_derecho = models.BooleanField(
        verbose_name='Mando Derecho',
        default=False
    )

    mando_izquierdo = models.BooleanField(
        verbose_name='Mando Izquierdo',
        default=False
    )

    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name='Cantidad',
        validators=[MinValueValidator(1)]
    )

    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Costo Unitario',
        default=0,
        validators=[MinValueValidator(0)]
    )

    costo_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Costo Total',
        default=0,
        validators=[MinValueValidator(0)]
    )

    costo_mano_obra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Costo Mano Obra',
        default=0,
        validators=[MinValueValidator(0)]
    )

    otros_costos = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Otros Costos',
        default=0,
        validators=[MinValueValidator(0)]
    )

    observaciones = models.TextField(
        verbose_name='Observaciones',
        null=True,
        blank=True
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Total',
        default=0,
        validators=[MinValueValidator(0)]
    )

    precio_venta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Precio Venta',
        default=0,
        validators=[MinValueValidator(0)]
    )

    ganancia_neta = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Ganancia Neta',
        default=0,
        validators=[MinValueValidator(0)]
    )

    ganancia_porcentaje = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='% Ganancia',
        default=0,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Cortina'
        verbose_name_plural = 'Cortinas'

    def __str__(self):
        return ''
