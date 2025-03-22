from django.urls import path
from .views import get_variables_config

urlpatterns = [
    path("get_variables_config/", get_variables_config, name="get_variables_config"),
]