from django.urls import path
from .views import ClienteCadastroView, logout_view, PrestadorCadastroView
app_name = 'usuarios'
urlpatterns = [
    path('cadastro/cliente/', ClienteCadastroView.as_view(), name='cadastro_cliente'),
    path('cadastro/prestador/', PrestadorCadastroView.as_view(), name='cadastro_prestador'),
    path('logout', logout_view, name='logout'),
]
