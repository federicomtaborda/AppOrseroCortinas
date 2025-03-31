import xlwt
from django.contrib import admin, messages
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from django.contrib.admin import SimpleListFilter

from unfold.decorators import display
from unfold.admin import ModelAdmin

from ordendetrabajo.models import OrdenTrabajo
from tipocortina.models import Cortina, TipoCortina, Modelo


@admin.register(Cortina)
class CortinaAdmin(ModelAdmin):
    autocomplete_fields = ['modelo', ]

    list_display = ('nombre', 'codigo', 'modelo', 'fabricacion_cortina', 'display_cortina',)

    search_fields = ['nombre', 'codigo']

    list_filter = ['tipo_cortina', 'modelo', 'fabricacion']

    fieldsets = (
        ('Descripción', {
            'fields': (('nombre', 'codigo'),),
        }),
        (None, {
            'fields': (('modelo', 'costo_m2'),)
        }),
        ('Tipo de Cortina - Fabricación', {
            'fields': (('tipo_cortina', 'fabricacion'),)
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

    @display(
        description=_("Fabricación Propia"),
        label={
            "SI": "success",
            "NO": "danger",
        },
    )
    def fabricacion_cortina(self, instance: Cortina):
        if instance.fabricacion:
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
    autocomplete_fields = ('articulo', 'orden_trabajo', 'mando', 'caida', 'tubo', 'ambiente')
    list_display = ('orden_trabajo', 'articulo', 'medidas', 'cantidad', 'total')
    actions = ['asignar_orden']
    list_filter = [OrdenTrabajoFilter, ]
    search_fields = ('orden_trabajo__contador',)

    fieldsets = (
        (None, {
            'fields': (('articulo', 'orden_trabajo'), 'ambiente',),
        }),
        ('Medidas - Cantidades', {
            'fields': (('ancho', 'alto', 'cantidad'),)
        }),
        (None, {
            'fields': (('mando', 'caida',),)
        }),
        (None, {
            'fields': (('tubo', 'ancho_tubo',),)
        }),
        ('Insumos - Materiales', {
            'fields': (('cadena', 'zocalo', 'tapa_zocalo', 'peso_cadena'),)
        }),
        (None, {
            'fields': (('tope', 'union', 'metros_totales'),)
        }),
        ('Costos', {
            'fields': (('costo', 'costo_mano_obra', 'otros_costos', 'costo_total'),)
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
        js = ('js/tipocortina_3.js',)

    # Si tiene Orden de Trabajo asignada es de solo lectura
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.orden_trabajo:
            return readonly_fields + ('orden_trabajo',)
        return readonly_fields

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
            # Sumar todos los campos 'total' de las cortinas seleccionadas
            suma_totales = sum(c.total for c in queryset if c.total is not None)

            # Crear la nueva orden con el total acumulado
            new_orden = OrdenTrabajo.objects.create(
                total=suma_totales
            )
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


# @admin.register(Stock)
# class StockAdmin(ModelAdmin):
#     autocomplete_fields = ('articulo',)
#     list_display = (
#         'articulo',
#         'metros_cuadrados',
#         'tipo_stock',
#         'fecha_stock'
#     )
#     list_filter = ('articulo', 'tipo_stock')
#     search_fields = ('articulo__nombre',)
#     fieldsets = (
#         ('Información Principal', {
#             'fields': (('articulo', 'metros_cuadrados'), 'tipo_stock',)
#         }),
#     )
#
#     def get_readonly_fields(self, request, obj=None):
#         # Si el objeto existe y el tipo_stock es 'EGRESO', hacer todos los campos readonly
#         if obj and obj.tipo_stock == TipoStock.EGRESO:
#             return [field.name for field in self.model._meta.fields]
#         return super().get_readonly_fields(request, obj)
#
#
#     actions = ['export_to_excel']
#
#     def export_to_excel(self, request, queryset):
#         # Crear un libro de trabajo y una hoja
#         wb = xlwt.Workbook(encoding='utf-8')
#         ws = wb.add_sheet('Stock')
#
#         # Definir estilos
#         header_style = xlwt.easyxf(
#             'font: bold on; align: horiz center;'
#         )
#         total_style = xlwt.easyxf(
#             'font: bold on, color red; align: horiz center;'
#         )
#
#         # Escribir los encabezados
#         headers = [
#             'Artículo',
#             'Metros Cuadrados',
#             'Cadena',
#             'Zócalo',
#             'Tapa Zócalo',
#             'Peso Cadena',
#             'Tope',
#             'Unión'
#         ]
#         for col, header in enumerate(headers):
#             ws.write(0, col, header, header_style)
#
#         # Escribir los datos
#         for row, stock in enumerate(queryset, start=1):
#             ws.write(row, 0, str(stock.articulo.nombre))
#             ws.write(row, 1, stock.metros_cuadrados)
#             ws.write(row, 2, stock.cadena)
#             ws.write(row, 3, stock.zocalo)
#             ws.write(row, 4, stock.tapa_zocalo)
#             ws.write(row, 5, stock.peso_cadena)
#             ws.write(row, 6, stock.tope)
#             ws.write(row, 7, stock.union)
#
#         # Calcular totales de todas las variables numéricas
#         total_metros_cuadrados = sum(stock.metros_cuadrados for stock in queryset if stock.metros_cuadrados is not None)
#         total_cadena = sum(stock.cadena for stock in queryset if stock.cadena is not None)
#         total_zocalo = sum(stock.zocalo for stock in queryset if stock.zocalo is not None)
#         total_tapa_zocalo = sum(stock.tapa_zocalo for stock in queryset if stock.tapa_zocalo is not None)
#         total_peso_cadena = sum(stock.peso_cadena for stock in queryset if stock.peso_cadena is not None)
#         total_tope = sum(stock.tope for stock in queryset if stock.tope is not None)
#         total_union = sum(stock.union for stock in queryset if stock.union is not None)
#
#         # Escribir los totales
#         total_row = [
#             'Total',
#             total_metros_cuadrados,
#             total_cadena,
#             total_zocalo,
#             total_tapa_zocalo,
#             total_peso_cadena,
#             total_tope,
#             total_union
#         ]
#         for col, value in enumerate(total_row):
#             ws.write(len(queryset) + 2, col, value, total_style)
#
#         # Crear una respuesta HTTP con el archivo Excel
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename=stock.xls'
#         wb.save(response)
#
#         return response
#
#     export_to_excel.short_description = "Exportar a Excel los elementos seleccionados"
