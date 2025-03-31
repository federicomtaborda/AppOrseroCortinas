from django.urls import path
from .views import get_variables_config, get_costo_m2, get_fabricacion

urlpatterns = [
    path("get_variables_config/", get_variables_config, name="get_variables_config"),

    path("costo_m2/<int:id_art>/", get_costo_m2, name="costo_m2"),
    path("get_fabricacion/<int:id_art>/", get_fabricacion, name="get_fabricacion"),
]