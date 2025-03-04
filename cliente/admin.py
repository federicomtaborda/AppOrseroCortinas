from django.contrib import admin
from unfold.admin import ModelAdmin

from cliente.models import Cliente, Colocador


@admin.register(Cliente)
class ClienteAdmin(ModelAdmin):
    list_display = ('razon_social', 'telefono',  'direccion', 'email', 'fecha_creacion', )
    search_fields = ['razon_social', ]

    fieldsets = (
        ('Cliente', {
            'fields': ('razon_social',),
        }),
        ('Dirección Télefono', {
            'fields': (('telefono',  'direccion'),),
        }),
        (None, {
            'fields': ('email',),
        }),
    )


@admin.register(Colocador)
class ColocadorAdmin(ModelAdmin):
    list_display = ('nombre', 'telefono', 'fecha_creacion')
    search_fields = ['nombre', ]

    fieldsets = (
        ('Colocador', {
            'fields': ('nombre',),
        }),
        (None, {
            'fields': ('telefono',),
        }),
    )
