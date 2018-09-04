from django.urls import path
from .views import SolicitacaoView

app_name = 'orcamentos'
urlpatterns = [
    path('solicitar/<str:slug>/', SolicitacaoView.as_view(), name='solicitar_orcamento'),
]
