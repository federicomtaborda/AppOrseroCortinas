from django.contrib import admin

from unfold.admin import ModelAdmin
from django.utils.html import format_html

from movimiento.models import Movimiento, TipoMovimiento


@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(ModelAdmin):
    list_display = ('nombre', 'egreso',)
    search_fields = ['nombre']
    ordering = ('nombre',)

    def get_readonly_fields(self, request, obj=None):
        # Si obj existe (edición), 'egreso' es de solo lectura
        if obj:
            return ['egreso']
        return []


@admin.register(Movimiento)
class MovimientoAdmin(ModelAdmin):
    autocomplete_fields = ['tipo_movimiento', ]
    ordering = ('-fecha',)
    list_display = ('numero_movimiento', 'fecha', 'tipo_movimiento',
                    'monto_negativo', 'detalle',)

    fieldsets = (
        (None, {
            'fields': (('tipo_movimiento', 'fecha'),)
        }),
        (None, {
            'fields': ('monto',),
        }),
        (None, {
            'fields': ('detalle',),
        }),
    )

    def monto_negativo(self, obj):
        if obj.monto < 0:
            return format_html('<span style="color: #d71c1c;">{}</span>', obj.monto)
        return format_html('<span style="color: #000000">{}</span>', obj.monto)
