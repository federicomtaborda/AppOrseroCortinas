import xlwt
from django.contrib import admin
from django.http import HttpResponse

from unfold.admin import ModelAdmin

from configuracion.opciones import TipoStock
from stock.models import StockCortinas, StockInsumos


@admin.register(StockCortinas)
class StockCortinasAdmin(ModelAdmin):
    list_display = (
        'articulo',
        'metros_cuadrados',
        'tipo_stock_cotinas',
        'fecha_stock_cortinas',
    )
    list_filter = ('articulo', 'tipo_stock_cotinas')
    search_fields = ('articulo',)
    fieldsets = (
        ('Información Principal', {
            'fields': (('articulo', 'metros_cuadrados'), 'tipo_stock_cotinas', 'fecha_stock_cortinas')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # Si el objeto existe y el tipo_stock es 'EGRESO', hacer todos los campos readonly
        if obj and obj.tipo_stock_cotinas == TipoStock.EGRESO:
            return [field.name for field in self.model._meta.fields]
        return super().get_readonly_fields(request, obj)


    actions = ['export_to_excel']

    def export_to_excel(self, request, queryset):
        # Crear un libro de trabajo y una hoja
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Stock')

        # Definir estilos
        header_style = xlwt.easyxf(
            'font: bold on; align: horiz center;'
        )
        total_style = xlwt.easyxf(
            'font: bold on, color red; align: horiz center;'
        )

        # Escribir los encabezados
        headers = [
            'Artículo',
            'Metros Cuadrados',
            'Cadena',
            'Zócalo',
            'Tapa Zócalo',
            'Peso Cadena',
            'Tope',
            'Unión'
        ]
        for col, header in enumerate(headers):
            ws.write(0, col, header, header_style)

        # Escribir los datos
        for row, stock in enumerate(queryset, start=1):
            ws.write(row, 0, str(stock.articulo.nombre))
            ws.write(row, 1, stock.metros_cuadrados)
            ws.write(row, 2, stock.cadena)
            ws.write(row, 3, stock.zocalo)
            ws.write(row, 4, stock.tapa_zocalo)
            ws.write(row, 5, stock.peso_cadena)
            ws.write(row, 6, stock.tope)
            ws.write(row, 7, stock.union)

        # Calcular totales de todas las variables numéricas
        total_metros_cuadrados = sum(stock.metros_cuadrados for stock in queryset if stock.metros_cuadrados is not None)
        total_cadena = sum(stock.cadena for stock in queryset if stock.cadena is not None)
        total_zocalo = sum(stock.zocalo for stock in queryset if stock.zocalo is not None)
        total_tapa_zocalo = sum(stock.tapa_zocalo for stock in queryset if stock.tapa_zocalo is not None)
        total_peso_cadena = sum(stock.peso_cadena for stock in queryset if stock.peso_cadena is not None)
        total_tope = sum(stock.tope for stock in queryset if stock.tope is not None)
        total_union = sum(stock.union for stock in queryset if stock.union is not None)

        # Escribir los totales
        total_row = [
            'Total',
            total_metros_cuadrados,
            total_cadena,
            total_zocalo,
            total_tapa_zocalo,
            total_peso_cadena,
            total_tope,
            total_union
        ]
        for col, value in enumerate(total_row):
            ws.write(len(queryset) + 2, col, value, total_style)

        # Crear una respuesta HTTP con el archivo Excel
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=stock.xls'
        wb.save(response)

        return response

    export_to_excel.short_description = "Exportar a Excel los elementos seleccionados"


@admin.register(StockInsumos)
class StockInismosAdmin(ModelAdmin):
    pass
