import datetime

from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

from AppOrsero import settings
from propietario.models import Propietario


def obtener_logo_propietario():
    return f"{settings.MEDIA_URL}{'logo.png'}"


def generar_pdf(template_name, context, request, filename="documento.pdf", inline=False):
    """
    Genera un PDF a partir de una plantilla HTML y un contexto por parametro.
    Agrega fecha, configuración de propietario y logo al contexto recibido.

    """
    context['fecha'] = datetime.date.today()
    context['propietario'] = Propietario.objects.first()
    context['logo'] = obtener_logo_propietario()

    try:
        html_string = render_to_string(template_name, context)
        html = HTML(string=html_string, base_url=request.build_absolute_uri())
        pdf_file = html.write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')

        disposition = 'inline' if inline else 'attachment'
        response['Content-Disposition'] = f'{disposition}; filename="{filename}"'

        return response
    except Exception as e:
        raise Exception(f"Error al generar el PDF: {e}")
