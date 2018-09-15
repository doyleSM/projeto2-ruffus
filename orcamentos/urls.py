from django.urls import path
from .views import SolicitacaoView, OrcamentoView, SolicitacoesAbertasListView, OrcamentosListViewSolicitacoes

app_name = 'orcamentos'
urlpatterns = [
    path('solicitar/<str:slug>/', SolicitacaoView.as_view(), name='solicitar_orcamento'),
    path('novo/<int:pk>/', OrcamentoView.as_view(), name='novo_orcamento'),
    path('solicitacoes-abertas/', SolicitacoesAbertasListView.as_view(), name='solicitacoes_abertas'),
    path('orcamentos/solicitacoes/<int:pk>/', OrcamentosListViewSolicitacoes.as_view(), name='orcamentos_solicitacoes'),
]
