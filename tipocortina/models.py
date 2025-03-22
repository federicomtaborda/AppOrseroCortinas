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


from django.db import models


class BaseTypeModel(models.Model):
    """
    Abstract base class for type models with common functionality
    """
    name = models.CharField(
        max_length=25,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.strip().capitalize()
        super().save(*args, **kwargs)


class Tipocaida(BaseTypeModel):
    class Meta:
        verbose_name = "Tipo de Caída"
        verbose_name_plural = "Tipos de Caída"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('name').verbose_name = "Tipo de Caída"


class Tipomando(BaseTypeModel):
    class Meta:
        verbose_name = "Tipo de Mando"
        verbose_name_plural = "Tipos de Mando"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('name').verbose_name = "Tipo de Mando"


class Tiptubo(BaseTypeModel):
    class Meta:
        verbose_name = "Tipo de Tubo"
        verbose_name_plural = "Tipos de Tubo"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('name').verbose_name = "Tipo de Tubo"


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

    mando = models.ForeignKey(
        Tipomando,
        verbose_name='Tipo de Mando',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    caida = models.ForeignKey(
        Tipocaida,
        verbose_name='Tipo de Caída',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    tubo = models.ForeignKey(
        Tiptubo,
        verbose_name='Tipo de Tubo',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    cadena = models.DecimalField(
        verbose_name='Cadena',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='valor calculado automáticamente'
    )

    zocalo = models.DecimalField(
        verbose_name='Zocalo',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='valor calculado automáticamente'
    )

    tapa_zocalo = models.IntegerField(
        verbose_name='Tapa Zocalo',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text='valor calculado automáticamente'
    )

    peso_cadena = models.IntegerField(
        verbose_name='Peso Cadena',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text='valor calculado automáticamente'
    )

    tope = models.IntegerField(
        verbose_name='Tope',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text='valor calculado automáticamente'
    )

    union = models.IntegerField(
        verbose_name='Unión',
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text='valor calculado automáticamente'
    )

    metros_totales = models.DecimalField(
        verbose_name='M² Tela ',
        validators=[MinValueValidator(0)],
        default=0,
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='valor calculado automáticamente'
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
        validators=[MinValueValidator(0)],
    )

    costo_total = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Costo Total',
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text='valor calculado automáticamente'
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
        validators=[MinValueValidator(0)],
        help_text='valor calculado automáticamente'
    )

    ganancia_neta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name='Ganancia Neta',
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text='valor calculado automáticamente'
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
