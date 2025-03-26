from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from configuracion.models import variablesModels
from tipocortina.models import Cortina


@login_required
def get_variables_config(request):
    """
    Vista para obtener todas las variables de configuración.
    Retorna una respuesta JSON con la lista de variables.
    """
    try:
        variables = variablesModels.objects.values()
        response_data = {
            'variables': list(variables),
        }
        return JsonResponse(response_data, status=200)

    except Exception as e:
        # Manejo básico de errores
        error_response = {
            'status': 'error',
            'message': str(e)
        }
        return JsonResponse(error_response, status=500)


@login_required
def get_costo_m2(request, id_art):
    """
    Obtiene solo el valor del costo por metro cuadrado de un artículo
    """
    try:
        articulo = Cortina.objects.get(id=id_art)
        return JsonResponse(articulo.costo_m2, safe=False, status=200)

    except Exception as e:
        error_response = {
            'status': 'error',
            'message': str(e)
        }
        return JsonResponse(error_response, status=500)
