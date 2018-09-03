from django.urls import path
from .views import ClienteCadastroView, logout_view, PrestadorCadastroView, PrestadorCategoriasView, Login


app_name = 'usuarios'
urlpatterns = [
    path('cadastro/cliente/', ClienteCadastroView.as_view(), name='cadastro_cliente'),
    path('cadastro/prestador/', PrestadorCadastroView.as_view(), name='cadastro_prestador'),
    path('cadastro/categorias/', PrestadorCategoriasView.as_view(), name='categorias_prestador'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
