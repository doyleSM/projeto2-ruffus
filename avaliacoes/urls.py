from django.urls import path
from .views import AvaliacaoView, AvaliacaoPeloPrestador

app_name = 'avaliacoes'
urlpatterns = [
    path('avaliar/<str:orcamentopk>/', AvaliacaoView.as_view(), name='avaliar'),
    path('avaliar-usuario/<int:orcamentopk>/', AvaliacaoPeloPrestador.as_view(), name='avaliar_cliente'),
]