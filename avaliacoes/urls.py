from django.urls import path
from .views import AvaliacaoView

app_name = 'avaliacoes'
urlpatterns = [
    path('avaliar/<str:orcamentopk>/', AvaliacaoView.as_view(), name='avaliar'),
]