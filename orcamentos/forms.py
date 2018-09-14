from django.forms import ModelForm
from .models import Solicitacao, Orcamento
from usuarios.models import Endereco

class SolicitacaoForm(ModelForm):

    class Meta:
        model = Solicitacao
        fields = ['descricao', 'endereco']

    def __init__(self, user, *args, **kwargs):
        super(SolicitacaoForm, self).__init__(*args, **kwargs)
        self.fields['endereco'].queryset = Endereco.objects.filter(usuario=user)


class OrcamentoForm(ModelForm):

    class Meta:
        model = Orcamento
        fields = ['descricao', 'valor']
