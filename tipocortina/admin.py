from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from django.contrib.admin import SimpleListFilter

from unfold.decorators import display
from unfold.admin import ModelAdmin

from ordendetrabajo.models import OrdenTrabajo
from tipocortina.models import Cortina, TipoCortina, Modelo, Stock


@admin.register(Cortina)
class CortinaAdmin(ModelAdmin):
    autocomplete_fields = ['modelo', ]

    list_display = ('nombre', 'codigo', 'modelo', 'display_cortina',)

    search_fields = ['nombre', 'codigo']

    list_filter = ['tipo_cortina', 'modelo']

    fieldsets = (
        ('Descripción', {
            'fields': (('nombre', 'codigo'),),
        }),
        (None, {
            'fields': (('modelo',),)
        }),
        ('Tipo de Cortina', {
            'fields': ('tipo_cortina',),
        }),
        (None, {
            'fields': ('caracteristicas',),
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
    search_fields = ['nombre']


class OrdenTrabajoFilter(SimpleListFilter):
    title = 'Orden de Trabajo'
    parameter_name = 'orden_trabajo'

    def lookups(self, request, model_admin):
        return (
            ('todas', 'Todas las Ordenes'),
            ('sin_orden', 'Sin Orden de Trabajo'),
            ('con_orden', 'Con Orden de Trabajo'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'sin_orden':
            return queryset.filter(orden_trabajo__isnull=True)
        if self.value() == 'con_orden':
            return queryset.filter(orden_trabajo__isnull=False)
        if self.value() == 'todas':
            return queryset
        return queryset.filter(orden_trabajo__isnull=True)


@admin.register(TipoCortina)
class TipoCortinaAdmin(ModelAdmin):
    autocomplete_fields = ('articulo', 'orden_trabajo', 'mando', 'caida', 'tubo',)
    list_display = ('orden_trabajo', 'articulo', 'medidas', 'cantidad', 'total')
    actions = ['asignar_orden']
    list_filter = (OrdenTrabajoFilter,)
    search_fields = ('orden_trabajo__contador',)

    fieldsets = (
        (None, {
            'fields': (('articulo', 'orden_trabajo'),),
        }),
        ('Medidas - Cantidades', {
            'fields': (('alto', 'ancho', 'cantidad'),)
        }),
        ('Mando - Caída - Tubo', {
            'fields': (('mando', 'caida', 'tubo'),)
        }),
        ('Otros Insumos', {
            'fields': (('cadena', 'zocalo', 'tapa_zocalo', 'peso_cadena'),)
        }),
        (None, {
            'fields': (('tope', 'union', 'metros_totales'),)
        }),
        ('Costos', {
            'fields': (('costo', 'costo_mano_obra', 'otros_costos', 'costo_total' ),)
        }),
        ('Totales - Ganancia', {
            'fields': (('ganancia_neta', 'ganancia_porcentaje', 'total'),)
        }),
        (None, {
            'fields': ('observaciones',)
        }),
    )

    class Media:
        css = {
            'all': ('css/tipocortina.css',)
        }
        js = ('js/tipocortina.js',)

    def has_delete_permission(self, request, obj=None):
        # No permite borrar si tiene orden asociada
        if obj is not None:
            if obj.orden_trabajo:
                return False
        return True

    def medidas(self, obj):
        return f"Alto: {obj.alto} - Ancho: {obj.ancho}"

    def asignar_orden(self, request, queryset):
        # Validar si hay cortinas seleccionadas
        if not queryset.exists():
            self.message_user(request, "No se seleccionaron cortinas.",
                              messages.WARNING)
            return HttpResponseRedirect(request.get_full_path())

        # Verificar si alguna cortina ya tiene una orden asignada
        if any(c.orden_trabajo is not None for c in queryset):
            self.message_user(request, "Algunas de las cortinas seleccionadas, "
                                       "ya tienen una orden de trabajo asignada. Verifique la asignación",
                              messages.WARNING)
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



@admin.register(Stock)
class StockAdmin(ModelAdmin):
    autocomplete_fields = ('articulo', )
    list_display = (
        'articulo',
        'metros_cuadrados',
        'cadena',
        'zocalo',
        'tapa_zocalo',
        'peso_cadena',
        'tope',
        'union'
    )
    list_filter = ('articulo',)
    search_fields = ('articulo__nombre',)
    fieldsets = (
        ('Información Principal', {
            'fields': ('articulo', 'metros_cuadrados')
        }),
        ('Detalles de Stock', {
            'fields': (
                'cadena',
                'zocalo',
                'tapa_zocalo',
                'peso_cadena',
                'tope',
                'union'
            )
        }),
    )

