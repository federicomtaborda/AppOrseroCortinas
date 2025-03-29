from django.contrib import admin, messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from configuracion.views import generar_pdf
from ordendetrabajo.models import OrdenTrabajo, EstadoOrden
from tipocortina.models import TipoCortina

from unfold.admin import ModelAdmin, TabularInline
from unfold.decorators import display


class TipoCortinaInline(TabularInline):
    fieldsets = (
        (None, {
            'fields': (
                ('articulo_descripcion', 'ancho', 'alto', 'cantidad', 'total'),
            )}),
    )

    readonly_fields = ('articulo_descripcion', 'ancho', 'alto', 'cantidad', 'total')

    model = TipoCortina
    extra = 0
    max_num = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(OrdenTrabajo)
class OrdenTrabajoAdmin(ModelAdmin):
    change_form_template = 'admin/custom/change_form.html'
    autocomplete_fields = ('cliente', 'colocador')
    list_display = ('numero_orden', 'cliente', 'colocador',
                    'fecha_format', 'fecha_entrega', 'dias_restantes', 'total', 'estado_orden', 'prioridad_state')
    list_editable = ('estado_orden',)
    list_filter = ('estado_orden', 'prioridad')
    search_fields = ('contador', 'cliente__razon_social',)
    inlines = [TipoCortinaInline]
    actions = ['generar_presupuesto', 'generar_orden_colocacion']
    ordering = ('-contador', '-fecha_creacion')

    fieldsets = (
        (None, {
            'fields': (('tipo_orden', 'prioridad'),)
        }),
        (None, {
            'fields': (('numero_orden', 'fecha_creacion', 'tiempo_entrega', 'estado_orden',),)
        }),
        (None, {
            'fields': (('cliente', 'colocador'),)
        }),
        (None, {
            'fields': ('total',)
        }),
        ('Observaciones', {
            'fields': ('observaciones',),
        }),
    )

    def fecha_format(self, obj):
        return obj.fecha_creacion.strftime('%d/%m/%Y')
    fecha_format.short_description = 'Fecha Orden'

    def fecha_entrega(self, obj):
        if obj and obj.tiempo_entrega:
            return obj.tiempo_entrega.strftime('%d/%m/%Y')
        return "-"
    fecha_entrega.short_description = 'Fecha Entrega'

    def dias_restantes(self, obj):
        if obj and obj.fecha_creacion and obj.tiempo_entrega:
            delta = obj.tiempo_entrega - obj.fecha_creacion
            dias = delta.days

            if dias < 5:  # Si faltan menos de 5 días, mostrar en rojo
                return format_html('<span style="color: red; font-weight: bold;">{}</span>', dias)
            else:
                return dias
        return "-"

    dias_restantes.short_description = 'Días Restantes'
    dias_restantes.admin_order_field = 'tiempo_entrega'

    @display(
        description=_("Prioridad"),
        label={
            "PRIORITARIO": "danger",
            "NORMAL": "info",
        },
    )
    def prioridad_state(self, instance: OrdenTrabajo):
        if instance.prioridad:
            return 'PRIORITARIO'
        else:
            return 'NORMAL'

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            if obj.estado_orden == EstadoOrden.TERMINADA:
                return ('numero_orden', 'prioridad', 'fecha_creacion', 'tiempo_entrega',
                        'metros_totales', 'cliente', 'colocador', 'cantidad',
                        'observaciones', 'tipo_orden', 'estado_orden', )
        return 'numero_orden', 'tipo_orden'

    class Media:
        css = {
            'all': ('css/orden_trabajo.css',)
        }
        js = ('js/orden_trabajo.js',)

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
        return generar_pdf("presupuesto.html", context, request, "presupuesto.pdf")
    generar_presupuesto.short_description = 'Generar Presupuesto'

    def generar_orden_colocacion(self, request, queryset):
        """
        Genera una orden de colocación con los datos proporcionados por el sistema.
        """
        if queryset.count() != 1:
            self.message_user(
                request,
                "Por favor, seleccione solo una Orden de trabajo para poder generar el detalle.",
                messages.WARNING
            )
            return HttpResponseRedirect(request.get_full_path())
        ordenes = []
        for o in queryset:
            ordenes = o
        cortinas = TipoCortina.objects.filter(orden_trabajo__in=queryset)
        total_cantidad = cortinas.aggregate(total_cantidad=Sum('cantidad'))['total_cantidad']
        context = {
            'orden': ordenes,
            'cortinas': cortinas,
            'total_cantidad': total_cantidad,

        }
        return generar_pdf("orden_colocacion.html", context, request, "orden_colocacion.pdf")
    generar_orden_colocacion.short_description = 'Generar Orden Colocación'

    def has_add_permission(self, request, obj=None):
        return False
