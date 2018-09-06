from django.urls import path
from .views import SolicitacaoView, OrcamentoView

app_name = 'orcamentos'
urlpatterns = [
    path('solicitar/<str:slug>/', SolicitacaoView.as_view(), name='solicitar_orcamento'),
    path('novo/', OrcamentoView.as_view(), name='novo_orcamento'),
]
