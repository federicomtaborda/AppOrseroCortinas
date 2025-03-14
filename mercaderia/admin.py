from django.contrib import admin
from .models import Mercaderia

from unfold.admin import ModelAdmin


@admin.register(Mercaderia)
class MercaderiaAdmin(ModelAdmin):
    autocomplete_fields = ('articulo', )
    list_display = ('articulo', 'metros_cuadrados', 'cantidad', 'costo', 'fecha_ingreso')
    search_fields = ('articulo__nombre',)
    list_filter = ('fecha_ingreso',)
    ordering = ('-fecha_ingreso',)

    fieldsets = (
        (None, {
            'fields': ('articulo',)
        }),
        ('Detalles', {
            'fields': (('metros_cuadrados', 'cantidad', 'costo'),)
        }),
        ('Información Adicional', {
            'fields': ('observaciones', )
        }),
    )