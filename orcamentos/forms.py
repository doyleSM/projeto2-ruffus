from django.forms import ModelForm
from .models import Solicitacao, Orcamento


class SolicitacaoForm(ModelForm):

    class Meta:
        model = Solicitacao
        fields = ['descricao', 'endereco']


class OrcamentoForm(ModelForm):

    class Meta:
        model = Orcamento
        fields = ['prestador', 'solicitacao', 'descricao', 'valor']