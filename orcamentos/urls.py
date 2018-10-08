from django.urls import path
from .views import SolicitacaoView, OrcamentoView, SolicitacoesAbertasListView, OrcamentosListViewSolicitacoes
from .views import aceitarOrcamento, cancelarSolicitacao, descartarOrcamento, restaurarOrcamento, OrcamentosPrestador
from .views import cancelarOrcamento, confimarRealizacao
app_name = 'orcamentos'
urlpatterns = [
    path('solicitar/<str:slug>/', SolicitacaoView.as_view(), name='solicitar_orcamento'),
    path('novo/<int:pk>/', OrcamentoView.as_view(), name='novo_orcamento'),
    path('solicitacoes-abertas/', SolicitacoesAbertasListView.as_view(), name='solicitacoes_abertas'),
    path('orcamentos/solicitacoes/<int:pk>/', OrcamentosListViewSolicitacoes.as_view(), name='orcamentos_solicitacoes'),
    path('aceitar-orcamento/<int:orcamentopk>/<int:solicitacaopk>/', aceitarOrcamento, name='aceitar-orcamento'),
    path('cancelar-solicitacao/<int:solicitacaopk>/', cancelarSolicitacao, name='cancelar-solicitacao'),
    path('descartar-orcamento/<int:orcamentopk>/', descartarOrcamento, name='descartar-orcamento'),
    path('restaurar-orcamento/<int:orcamentopk>/', restaurarOrcamento, name='restaurar-orcamento'),
    path('orcamentos-dados/', OrcamentosPrestador.as_view(), name='orcamentos-dados'),
    path('cancelar-orcamento/<int:orcamentopk>/', cancelarOrcamento, name='cancelar-orcamento'),
    path('confirma-realizacao/<int:orcamentopk>/', confimarRealizacao, name='confirma-realizacao'),

]
