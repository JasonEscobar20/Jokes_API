from django.urls import path

from core_api.views import ListarDatos

app_name = 'jokes_api'

urlpatterns = [
    path('listar_datos/', ListarDatos.as_view(), name='listar-datos'),
]