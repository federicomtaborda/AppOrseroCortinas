from django.contrib import admin

from unfold.admin import ModelAdmin
from django.utils.html import format_html

from movimiento.models import Movimiento, TipoMovimiento


@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(ModelAdmin):
    list_display = ('nombre', 'descuenta_saldo', )

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Movimiento)
class MovimientoAdmin(ModelAdmin):
    list_display = ('numero_movimiento', 'fecha', 'tipo_movimiento',
                    'cliente', 'orden_trabajo',
                    'monto_negativo', 'detalle',)

    fieldsets = (
        (None, {
            'fields': (('tipo_movimiento', 'fecha'),)
        }),
        (None, {
            'fields': ('cliente',),
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
        return obj.monto
