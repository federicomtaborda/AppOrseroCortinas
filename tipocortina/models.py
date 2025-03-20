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


TIPOCAIDA = [
    ('Normal', 'Normal'),
    ('invertida', 'Invertida'),
]

TIPOMANDO = [
    ('derecho', 'Mando Derecho'),
    ('izquierdo', 'Mando Izquierdo'),
]


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

    articulo_descripcion = models.CharField(
        verbose_name='Art Descripción',
        max_length=180,
        null=True,
        blank=True
    )

    orden_trabajo = models.ForeignKey(
        OrdenTrabajo,
        verbose_name='Orden Trabajo',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    alto = models.DecimalField(
        verbose_name='Alto (mts)',
        max_digits=20,
        validators=[MinValueValidator(0)],
        decimal_places=2,
        default=0.00
    )

    ancho = models.DecimalField(
        verbose_name='Ancho (mts)',
        max_digits=20,
        validators=[MinValueValidator(0)],
        decimal_places=2,
        default=0.00
    )

    metros_cuadrados = models.IntegerField(
        verbose_name='Metros²',
        validators=[MinValueValidator(0)],
        default=0
    )

    mando = models.CharField(
        verbose_name='Mando',
        max_length=100,
        choices=TIPOMANDO,
        default='',
        null=True,
        blank=True
    )

    caida = models.CharField(
        verbose_name='Caída',
        max_length=100,
        choices=TIPOCAIDA,
        default='',
        null=True,
        blank=True
    )

    cantidad = models.PositiveIntegerField(
        default=1,
        verbose_name='Cantidad',
        validators=[MinValueValidator(1)]
    )

    costo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Costo Unitario',
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    costo_total = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Costo Total',
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    costo_mano_obra = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Costo Mano Obra',
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    otros_costos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Otros Costos',
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    observaciones = models.TextField(
        verbose_name='Observaciones',
        null=True,
        blank=True
    )

    total = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Total',
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    ganancia_neta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Ganancia Neta',
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    ganancia_porcentaje = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='% Ganancia',
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Cortina'
        verbose_name_plural = 'Cortinas'

    def __str__(self):
        return ''

    def save(self, *args, **kwargs):
        self.articulo_descripcion = str(self.articulo)
        super().save(*args, **kwargs)
