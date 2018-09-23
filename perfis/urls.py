from django.urls import path
from .views import PerfilPrestador
app_name = 'perfis'
urlpatterns = [
    path('/prestador/', PerfilPrestador.as_view(), name='prefil_prestador'),
]