from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import TemplateView

from unfold.views import UnfoldModelAdminViewMixin

from ordendetrabajo.models import OrdenTrabajo, TipoOrden
from reportes.forms import ReporteVentasForm, TipoReporte

import xlwt


# Styles
BOLD_STYLE = xlwt.XFStyle()
BOLD_STYLE.font.bold = True
DEFAULT_STYLE = xlwt.XFStyle()

# Constants
CONTENT_TYPE = 'application/ms-excel'
RESPONSE = HttpResponse(content_type=CONTENT_TYPE)
DATE_FORMAT = '%d/%m/%Y'


def generate_filename(report_type: str, fecha_desde, fecha_hasta) -> str:
    """Generate filename based on report type and date range"""
    formatted_start = fecha_desde.strftime(DATE_FORMAT)
    formatted_end = fecha_hasta.strftime(DATE_FORMAT)
    return f"{report_type} - {formatted_start}_{formatted_end}.xls"


def set_content_disposition(filename):
    return f'attachment; filename={filename}'


def write_headers(worksheet, columns, style):
    """
    Escribe encabezados en la primera fila de una hoja de Excel.
    """
    for col, header in enumerate(columns):
        worksheet.write(0, col, header, style)


def reporte_ventas_xls(fecha_desde, fecha_hasta):

    WORKBOOK = xlwt.Workbook(encoding='utf-8')
    SHEET_NAME = 'Reporte'
    WORKSHEET = WORKBOOK.add_sheet(SHEET_NAME)

    COLUMNS = ['Orden', 'Tipo', 'Fecha', 'Cliente', 'Colocador', 'Estado Ord.', 'Total']

    filename = generate_filename('Resumen de ventas', fecha_desde, fecha_hasta)

    sales_orders = (OrdenTrabajo.objects
                    .filter(tipo_orden__in=[TipoOrden.VENTA],
                            fecha_creacion__range=(fecha_desde, fecha_hasta))
                    .select_related('cliente', 'colocador')
                    .order_by('fecha_creacion', 'id'))

    # Initialize response and workbook
    RESPONSE['Content-Disposition'] = set_content_disposition(filename)

    write_headers(WORKSHEET, COLUMNS, BOLD_STYLE)

    # Write data
    total = 0
    for row, order in enumerate(sales_orders, 1):  # Start from row 1
        row_data = [
            order.numero_orden,
            str(order.tipo_orden),
            order.fecha_creacion.strftime(DATE_FORMAT),
            order.cliente.razon_social,
            order.colocador.nombre,
            str(order.estado_orden),
            float(order.total) if order.total else 0.0,]

        total += row_data[-1]  # Add to total

        for col, value in enumerate(row_data):
            WORKSHEET.write(row, col, value, DEFAULT_STYLE)

    # Write total
    total_row = len(sales_orders) + 2
    WORKSHEET.write(total_row, 6, 'Total Vendido', BOLD_STYLE)
    WORKSHEET.write(total_row, 7, total, DEFAULT_STYLE)

    # Add total sales count
    count_row = total_row + 1
    WORKSHEET.write(count_row, 6, 'Cantidad de Ventas', BOLD_STYLE)
    WORKSHEET.write(count_row, 7, len(sales_orders), DEFAULT_STYLE)

    WORKBOOK.save(RESPONSE)
    return RESPONSE


class ReportVentasView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Reportes"
    permission_required = ()
    template_name = "reportes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReporteVentasForm()
        return context

    def post(self, request, *args, **kwargs):
        form = ReporteVentasForm(request.POST)
        if form.is_valid():
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            tipo = form.cleaned_data['tipo']
            if tipo == TipoReporte.VENTAS:
                return reporte_ventas_xls(fecha_desde, fecha_hasta)
            elif tipo == TipoReporte.MOVIMIENTOS:
                return reporte_movimientos_xls(fecha_desde, fecha_hasta)
        else:
            messages.error(request, "El formulario no es válido. Por favor, revisa los datos ingresados.")
            return self.render_to_response(self.get_context_data(form=form))
