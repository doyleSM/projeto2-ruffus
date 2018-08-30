# -*- coding: utf 8 -*-


from django.urls import path
from .views import lista_servicos, lista_por_categoria, detalhe_servico, get_categorias

app_name = 'catalogo'
urlpatterns = [
    path('', lista_servicos, name='lista_servicos'),
    path('<str:slug>/', lista_por_categoria, name='lista_por_categoria'),
    path('detalhe/<str:slug>/', detalhe_servico, name='detalhe_servico'),
    path('api/categorias/', get_categorias, name='api_categorias'),
]
