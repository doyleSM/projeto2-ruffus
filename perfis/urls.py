from django.urls import path
from .views import PerfilPrestador, PerfilCliente
app_name = 'perfis'
urlpatterns = [
    path('prestador/<int:pk>/', PerfilPrestador.as_view(), name='prefil_prestador'),
    path('cliente/<int:pk>/', PerfilCliente.as_view(), name='perfil_cliente'),
]