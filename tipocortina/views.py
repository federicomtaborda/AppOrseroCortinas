from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from configuracion.models import variablesModels


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
