from decimal import Decimal
from operator import is_not

from django.core.validators import MinValueValidator
from django.db import models

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from configuracion.opciones import TipoStock, EstadoStock
from ordendetrabajo.models import OrdenTrabajo
from stock.models import StockCortinas


class Modelo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Modelo')

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        super(Modelo, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre}"


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

        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_tipocaidae_name')
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('name').verbose_name = "Tipo de Caída"


class Tipomando(BaseTypeModel):
    class Meta:
        verbose_name = "Tipo de Mando"
        verbose_name_plural = "Tipos de Mando"

        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_tipomando_name')
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('name').verbose_name = "Tipo de Mando"


class Tipotubo(BaseTypeModel):
    class Meta:
        verbose_name = "Tipo de Tubo"
        verbose_name_plural = "Tipos de Tubo"

        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_tipotubo_name')
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('name').verbose_name = "Tipo de Tubo"


class Ambiente(BaseTypeModel):
    class Meta:
        verbose_name = "Ambiente"
        verbose_name_plural = "Ambientes"

        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_ambiente_name')
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.get_field('name').verbose_name = "Ambiente"


class Cortina(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Cortina')
    codigo = models.CharField(max_length=25, verbose_name='Código', null=True, blank=True)
    modelo = models.ForeignKey(Modelo, verbose_name='Modelo', on_delete=models.PROTECT)
    costo_m2 = models.DecimalField(verbose_name='Costo M²', max_digits=10, validators=[MinValueValidator(0)],
                                   decimal_places=2, default=0.00)
    caracteristicas = models.TextField(verbose_name='Caracteristicas', null=True, blank=True)
    fabricacion = models.BooleanField(verbose_name='Fabricación Propia', default=False)
    tipo_cortina = models.BooleanField(verbose_name='Cortina de Confección', default=False)

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

    ambiente = models.ForeignKey(
        Ambiente,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='ambiente',
    )

    orden_trabajo = models.ForeignKey(
        OrdenTrabajo,
        verbose_name='Orden Trabajo',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='orden_tipocortina'
    )

    alto = models.DecimalField(
        verbose_name='Alto (mts)',
        max_digits=10,
        validators=[MinValueValidator(0)],
        decimal_places=2,
        default=0.00
    )

    ancho = models.DecimalField(
        verbose_name='Ancho (mts)',
        max_digits=10,
        validators=[MinValueValidator(0)],
        decimal_places=2,
        default=0.00
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
        Tipotubo,
        verbose_name='Tipo de Tubo',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    ancho_tubo = models.DecimalField(
        verbose_name='Ancho Tubo (mts)',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        default=0.00
    )

    cadena = models.DecimalField(
        verbose_name='Cadena',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        default=0.00,
        help_text='valor calculado automáticamente'
    )

    zocalo = models.DecimalField(
        verbose_name='Zocalo (mts)',
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        default=0.00,
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
        default=0.00,
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='valor calculado automáticamente'
    )

    cantidad = models.PositiveIntegerField(
        default=0,
        verbose_name='Cantidad',
        validators=[MinValueValidator(1)]
    )

    costo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Costo Unitario',
        default=0.00,
        validators=[MinValueValidator(0)],
    )

    costo_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Costo Total',
        default=0.00,
        validators=[MinValueValidator(0)],
        help_text='valor calculado automáticamente'
    )

    costo_mano_obra = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Costo Mano Obra',
        default=0.00,
        validators=[MinValueValidator(0)]
    )

    otros_costos = models.DecimalField(
        max_digits=10,
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


# actualiza Orden de trabajo al crear una nueva y asignarla
@receiver(pre_save, sender=TipoCortina)
def recalcular_total(sender, instance, **kwargs):
    # Si no tiene orden de trabajo asociada, no hacemos nada
    if not instance.orden_trabajo:
        return

    try:
        # Obtenemos todas las cortinas asociadas a esta orden (excluyendo la actual si ya existe)
        cortinas = TipoCortina.objects.filter(orden_trabajo=instance.orden_trabajo)

        # Sumamos los totales de todas las cortinas existentes más el nuevo valor
        total = sum(c.total for c in cortinas) + instance.total

        # Actualizamos el total en la orden de trabajo
        orden = instance.orden_trabajo
        orden.total = total
        orden.save()

    except OrdenTrabajo.DoesNotExist:
        return


# actualiza Orden de trabajo al eliminar una orden existente
@receiver(pre_delete, sender=TipoCortina)
def actualizar_total_al_eliminar(sender, instance, **kwargs):
    if instance.orden_trabajo:
        try:
            # Obtenemos la orden de trabajo asociada
            orden = instance.orden_trabajo

            # Restamos el total de la cortina que se está eliminando
            orden.total -= instance.total

            # Guardamos la orden con el nuevo total
            orden.save()
        except OrdenTrabajo.DoesNotExist:
            pass


@receiver(post_save, sender=TipoCortina)
def actualizar_stock(sender, instance, created, **kwargs):
    """
    Actualiza el stock de cortinas cuando se crea o modifica una instancia.
    Para ambos casos (creación o actualización), se registra un egreso de stock.

    Verifica si el tipo de cortina es de Fabricación propia
    """
    if not instance.articulo.fabricacion:
        return

    if sender.__name__ != "TipoCortina":
        return

    stock, created_stock = StockCortinas.objects.update_or_create(
        pk=instance.pk,
        defaults={
            'metros_cuadrados': -instance.metros_totales,
            'articulo': instance.articulo_descripcion,
            'estado_stock_cortinas': EstadoStock.COMPROMETIDO,
            'tipo_stock_cotinas': TipoStock.EGRESO
        }
    )


@receiver(pre_delete)
def borrar_stock(sender, instance, **kwargs):
    """
    Borra el registro de StockCortinas cuando se elimina la instancia relacionada.
    """

    if sender.__name__ != "TipoCortina":
        return

    try:
        stock = StockCortinas.objects.get(pk=instance.pk)
        stock.delete()
    except StockCortinas.DoesNotExist:
        pass  # No hay stock asociado para borrar
