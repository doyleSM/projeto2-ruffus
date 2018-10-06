from django.forms import ModelForm, Textarea
from .models import Avaliacao

class AvaliacaoForm(ModelForm):

    class Meta:
        model = Avaliacao
        fields = ['comentario', 'nota']
        widgets = {
            'comentario': Textarea(attrs={'cols': 40, 'rows': 5, }),
        }
        labels = {
            'comentario': ('Deixe sua avaliação sobre serviço realizado e dê uma nota logo abaixo'),

        }