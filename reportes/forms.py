
from django import forms
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminSingleDateWidget


class TipoReporte:
    VENTAS = 'ventas'
    MOVIMIENTOS = 'movimientos'


TIPO_REPORTE = (
    (TipoReporte.VENTAS, u'Ventas'),
    (TipoReporte.MOVIMIENTOS, u'Movimientos'),
)


class ReporteVentasForm(forms.Form):
    tipo = forms.ChoiceField(label='Elija un tipo de Reporte', choices=TIPO_REPORTE, initial=TipoReporte.VENTAS,
                             widget=UnfoldAdminSelectWidget, required=True)
    fecha_desde = forms.DateField(
        label=u'Fecha Desde',
        required=True,
        widget=UnfoldAdminSingleDateWidget(attrs={
            "type": "date",
        },),
        input_formats=["%Y-%m-%d"],
    )
    fecha_hasta = forms.DateField(
        label='Fecha Hasta',
        required=True,
        widget=UnfoldAdminSingleDateWidget(attrs={
            "type": "date",
        }, ),
        input_formats=["%Y-%m-%d"],
    )