from django.forms import ModelForm, Textarea
from .models import Solicitacao, Orcamento
from usuarios.models import Endereco
from django.utils.translation import gettext_lazy as _


class SolicitacaoForm(ModelForm):

    class Meta:
        model = Solicitacao
        fields = ['descricao', 'endereco']
        widgets = {
            'descricao': Textarea(attrs={'cols': 40, 'rows': 5, }),
        }
        labels = {
            'descricao': _('Descreva o que você precisa'),

        }

    def __init__(self, user, *args, **kwargs):
        super(SolicitacaoForm, self).__init__(*args, **kwargs)
        self.fields['endereco'].queryset = Endereco.objects.filter(usuario=user)


class OrcamentoForm(ModelForm):

    class Meta:
        model = Orcamento
        fields = ['descricao', 'valor']

