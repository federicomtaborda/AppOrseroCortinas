from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from unfold.decorators import display
from unfold.admin import ModelAdmin

from ordendetrabajo.models import OrdenTrabajo
from tipocortina.models import Cortina, TipoCortina, Modelo


@admin.register(Cortina)
class CortinaAdmin(ModelAdmin):
    list_display = ('nombre', 'codigo', 'modelo', 'display_cortina',)

    search_fields = ['nombre', 'codigo']

    list_filter = ['tipo_cortina', 'modelo']

    fieldsets = (
        ('Descripción', {
            'fields': (('nombre', 'codigo'), 'modelo'),
        }),
        ('Tipo de Cortina', {
            'fields': ('tipo_cortina',),
        }),
        ('Caracteristicas', {
            'fields': ('observaciones',),
        }),
    )

    @display(
        description=_("Cortina de Confección"),
        label={
            "SI": "success",
            "NO": "danger",
        },
    )
    def display_cortina(self, instance: Cortina):
        if instance.tipo_cortina:
            return 'SI'
        else:
            return 'NO'


@admin.register(Modelo)
class TipoCortinaAdmin(ModelAdmin):
    list_display = ('nombre',)


@admin.register(TipoCortina)
class TipoCortinaAdmin(ModelAdmin):
    autocomplete_fields = ('articulo', 'orden_trabajo', )
    list_display = ('orden_trabajo', 'articulo', 'medidas', 'cantidad', 'total')
    actions = ['asignar_orden']

    fieldsets = (
        (None, {
            'fields': (('articulo', 'orden_trabajo'),),
        }),
        ('Medidas - Cantidades', {
            'fields': (('alto', 'ancho', 'cantidad'),)
        }),
        ('Mando Maniobra', {
            'fields': (('mando_derecho', 'mando_izquierdo'),)
        }),
        ('Costos', {
            'fields': (('costo', 'costo_mano_obra', 'otros_costos', 'costo_total' ),)
        }),
        ('Totales - Ganancia', {
            'fields': (('total', 'ganancia_neta', 'ganancia_porcentaje', ),)
        }),
        (None, {
            'fields': ('observaciones',)
        }),
    )

    readonly_fields = ('total', 'costo_total', 'ganancia_neta', 'metros_cuadrados', )

    def medidas(self, obj):
        return f"Alto: {obj.alto} - Ancho: {obj.ancho}"

    def asignar_orden(self, request, queryset):
        # Validar si hay cortinas seleccionadas
        if not queryset.exists():
            self.message_user(request, "No se seleccionaron cortinas.", messages.WARNING)
            return HttpResponseRedirect(request.get_full_path())

        # Verificar si alguna cortina ya tiene una orden asignada
        if any(c.orden_trabajo is not None for c in queryset):
            self.message_user(request, "Algunas de las cortinas seleccionadas, "
                                       "ya tienen una orden de trabajo asignada. Verifique la asignación", messages.WARNING)
            return HttpResponseRedirect(request.get_full_path())

        # Crear y asignar la nueva orden en una transacción atómica
        with transaction.atomic():
            new_orden = OrdenTrabajo.objects.create()
            queryset.update(orden_trabajo=new_orden)

        # Mostrar mensaje de éxito con detalles
        self.message_user(
            request,
            f"Se asignó la orden de trabajo {new_orden} a {queryset.count()} cortina/s.",
            messages.SUCCESS
        )
        return HttpResponseRedirect(request.get_full_path())

    # Actualizar la descripción corta
    asignar_orden.short_description = 'Asignar nueva orden de trabajo'


