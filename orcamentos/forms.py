from django.forms import ModelForm
from .models import Solicitacao


class SolicitacaoForm(ModelForm):

    class Meta:
        model = Solicitacao
        fields = ['cliente', 'servico', 'endereco', 'descricao']
