from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import TemplateView

from unfold.views import UnfoldModelAdminViewMixin

from movimiento.models import Movimiento
from ordendetrabajo.models import OrdenTrabajo, TipoOrden, EstadoOrden
from reportes.forms import ReporteVentasForm, TipoReporte

import xlwt

from tipocortina.models import TipoCortina

# Styles
BOLD_STYLE = xlwt.XFStyle()
BOLD_STYLE.font.bold = True
DEFAULT_STYLE = xlwt.XFStyle()

# Constants
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

    CONTENT_TYPE = 'application/ms-excel'
    RESPONSE = HttpResponse(content_type=CONTENT_TYPE)

    COLUMNS = ['Orden', 'Tipo', 'Fecha', 'Cliente', 'Colocador', 'Estado Ord.', 'Total', 'Ganancia Neta']

    filename = generate_filename('Resumen de ventas', fecha_desde, fecha_hasta)

    sales_orders = (OrdenTrabajo.objects
                    .filter(tipo_orden__in=[TipoOrden.VENTA], estado_orden=EstadoOrden.TERMINADA,
                            fecha_creacion__range=(fecha_desde, fecha_hasta))
                    .select_related('cliente', 'colocador')
                    .order_by('fecha_creacion', 'id'))

    ganancia = TipoCortina.objects.filter(orden_trabajo__in=sales_orders)

    # Initialize response and workbook
    RESPONSE['Content-Disposition'] = set_content_disposition(filename)

    write_headers(WORKSHEET, COLUMNS, BOLD_STYLE)

    # Write data
    total_general = 0
    total_ganancia = 0
    for row, order in enumerate(sales_orders, 1):  # Start from row 1
        # Calcula la sumatoria de la ganancia neta
        order_ganancia_total = sum(
            float(ganancia.ganancia_neta) if ganancia.ganancia_neta else 0.0
            for ganancia in ganancia.filter(orden_trabajo=order)
        )

        row_data = [
            order.numero_orden,
            str(order.tipo_orden),
            order.fecha_creacion.strftime(DATE_FORMAT),
            str(order.cliente.razon_social if order.cliente else ''),
            str(order.colocador.nombre if order.colocador else ''),
            str(order.estado_orden),
            float(order.total) if order.total else 0.0,
            order_ganancia_total,
        ]

        total_general += row_data[-2]
        total_ganancia += row_data[-1]

        for col, value in enumerate(row_data):
            WORKSHEET.write(row, col, value, DEFAULT_STYLE)

    # Total vendido
    total_row = len(sales_orders) + 2
    WORKSHEET.write(total_row, 6, 'Total Vendido', BOLD_STYLE)
    WORKSHEET.write(total_row, 7, total_general, DEFAULT_STYLE)

    # Total ganancia
    count_row = total_row + 1
    WORKSHEET.write(count_row, 6, 'Total Ganancia Neta', BOLD_STYLE)
    WORKSHEET.write(count_row, 7, total_ganancia, DEFAULT_STYLE)

    # cantidad de ventas
    count_row = count_row + 1
    WORKSHEET.write(count_row, 6, 'Cantidad de Ventas', BOLD_STYLE)
    WORKSHEET.write(count_row, 7, len(sales_orders), DEFAULT_STYLE)

    WORKBOOK.save(RESPONSE)
    return RESPONSE


def reporte_movimientos_xls(fecha_desde, fecha_hasta):

    WORKBOOK = xlwt.Workbook(encoding='utf-8')
    SHEET_NAME = 'Reporte'
    WORKSHEET = WORKBOOK.add_sheet(SHEET_NAME)

    CONTENT_TYPE = 'application/ms-excel'
    RESPONSE = HttpResponse(content_type=CONTENT_TYPE)

    COLUMNS = ['N° Movimiento', 'Fecha', 'Tipo', 'Detalle', 'Monto']

    # Define styles
    BOLD_STYLE = xlwt.easyxf('font: bold on;')
    DEFAULT_STYLE = xlwt.easyxf('')
    RED_STYLE = xlwt.easyxf('font: color red;')

    filename = generate_filename('Resumen de movimientos', fecha_desde, fecha_hasta)

    movimientos = Movimiento.objects.filter().order_by('fecha', 'id')

    # Initialize response and workbook
    RESPONSE['Content-Disposition'] = set_content_disposition(filename)

    for col, header in enumerate(COLUMNS):
        WORKSHEET.write(0, col, header, BOLD_STYLE)

    # Write data
    total = 0
    for row, movimiento in enumerate(movimientos, 1):
        row_data = [
            str(movimiento.numero_movimiento),
            movimiento.fecha.strftime(DATE_FORMAT),
            str(movimiento.tipo_movimiento),
            str(movimiento.detalle),
            float(movimiento.monto) if movimiento.monto else 0.0,
        ]

        total += row_data[-1]

        for col, value in enumerate(row_data):

            # Apply red style to monto if negative
            if col == 4 and value < 0:  # 4 is the 'Monto' column index
                WORKSHEET.write(row, col, value, RED_STYLE)
            else:
                WORKSHEET.write(row, col, value, DEFAULT_STYLE)

    # Write total
    total_row = len(movimientos) + 2
    WORKSHEET.write(total_row, 5, 'Total Movimientos', BOLD_STYLE)
    WORKSHEET.write(total_row, 6, total, DEFAULT_STYLE)

    # Add total sales count
    count_row = total_row + 1
    WORKSHEET.write(count_row, 5, 'Cantidad de Movimientos', BOLD_STYLE)
    WORKSHEET.write(count_row, 6, len(movimientos), DEFAULT_STYLE)

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
