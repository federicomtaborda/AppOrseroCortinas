from django.contrib import admin
from django.urls import path

from unfold.admin import ModelAdmin

from propietario.models import Propietario
from reportes.views import ReportVentasView


@admin.register(Propietario)
class PropietarioAdmin(ModelAdmin):
    # Campos que se mostrarán en la lista
    list_display = ('nombre', 'direccion', 'telefono', 'ciudad', 'cod_postal', 'email', 'cbu')

    fieldsets = (
        (None, {
            'fields': (('nombre',),)
        }),
        (None, {
            'fields': (('direccion', 'ciudad', 'cod_postal'),)
        }),
        (None, {
            'fields': (('telefono', 'email'),)
        }),
        (None, {
            'fields': ('cbu',)
        }),
    )

    def has_add_permission(self, request):
        if Propietario.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if Propietario.objects.exists():
            return False
        return True


    def get_urls(self):
        return super().get_urls() + [
            path(
                "reportes",
                ReportVentasView.as_view(model_admin=self),
                name="reportes",
            ),
        ]
