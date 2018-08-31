from django.urls import path
from .views import ClienteCadastroView, logout_view
app_name = 'usuarios'
urlpatterns = [
    path('cadastro/cliente/', ClienteCadastroView.as_view(), name='cadastro_cliente'),
    path('logout', logout_view, name='logout'),
]
