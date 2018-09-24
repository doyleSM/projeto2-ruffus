from django.forms import ModelForm
from .models import Avaliacao

class AvaliacaoForm(ModelForm):

    class Meta:
        model = Avaliacao
        fields = ['comentario', 'nota']