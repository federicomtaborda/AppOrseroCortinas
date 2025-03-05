from django.contrib import admin, messages
from django.http import HttpResponseRedirect

from configuracion.views import generar_pdf
from ordendetrabajo.models import OrdenTrabajo
from tipocortina.models import TipoCortina
from unfold.admin import ModelAdmin, TabularInline


class TipoCortinaInline(TabularInline):
    fieldsets = (
        (None, {
            'fields': (
                ('articulo', 'alto', 'ancho', 'metros_cuadrados', 'cantidad', 'precio_venta'),
            )}),
    )
    readonly_fields = ('articulo', 'alto', 'ancho', 'metros_cuadrados', 'cantidad', 'precio_venta')
    model = TipoCortina
    extra = 0
    max_num = 0

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(ModelAdmin):
    change_form_template = 'admin/custom/change_form.html'
    autocomplete_fields = ('cliente', 'colocador')
    list_display = ('numero_orden', 'cliente', 'fecha_creacion', 'estado_orden',)
    list_editable = ('estado_orden',)
    list_filter = ('estado_orden', )
    search_fields = ('contador', 'cliente__razon_social')
    inlines = [TipoCortinaInline]
    actions = ['generar_presupuesto']
    ordering = ('-contador',)

    fieldsets = (
        (None, {
            'fields': (('tipo_orden',),)
        }),
        (None, {
            'fields': (('numero_orden', 'fecha_creacion', 'tiempo_entrega', 'estado_orden',),)
        }),
        (None, {
            'fields': (('cliente', 'colocador'),)
        }),
        (None, {
            'fields': (('metros_totales', 'total'),)
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
        }),
    )

    readonly_fields = ('numero_orden', 'fecha_creacion', 'tipo_orden', 'metros_totales', 'total', )

    def generar_presupuesto(self, request, queryset):
        """
        Genera un presupuesto en PDF para una única orden de trabajo seleccionada.
        """
        # Validar que se haya seleccionado exactamente una orden
        if queryset.count() != 1:
            self.message_user(
                request,
                "Por favor, seleccione solo una Orden de Trabajo para generar el presupuesto.",
                messages.WARNING
            )
            return HttpResponseRedirect(request.get_full_path())

        orden = queryset.first()
        cortinas = list(TipoCortina.objects.filter(orden_trabajo=orden))

        context = {
            'orden': orden,
            'cortinas': cortinas,
        }
        return generar_pdf("orden_trabajo.html", context, request, "orden_trabajo.pdf")

    generar_presupuesto.short_description = 'Generar Presupuesto'

    def has_add_permission(self, request, obj=None):
        return False
