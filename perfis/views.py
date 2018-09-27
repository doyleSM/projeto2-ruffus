from usuarios.models import Prestador
from django.views.generic import ListView
from orcamentos.models import Solicitacao
from avaliacoes.models import Avaliacao
# Create your views here.

class PerfilPrestador(ListView):

    template_name = 'perfis/perfil_prestador.html'
    context_object_name = 'perfil'

    #paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super(PerfilPrestador, self).get_context_data(**kwargs)
        context['completos'] = Solicitacao.objects.filter(status=5, orcamento_aceito__prestador=self.kwargs['pk']).count()
        context['avaliacoes'] = Avaliacao.objects.filter(orcamento__prestador=self.kwargs['pk'])
        avaliacoes = Avaliacao.objects.filter(orcamento__prestador=self.kwargs['pk'])
        nota1 = avaliacoes.filter(nota=1).count()
        nota2 = avaliacoes.filter(nota=2).count()
        nota3 = avaliacoes.filter(nota=3).count()
        nota4 = avaliacoes.filter(nota=4).count()
        nota5 = avaliacoes.filter(nota=5).count()
        nota = 0
        total_avaliacoes = avaliacoes.count()

        for avaliacao in avaliacoes:
            nota += avaliacao.nota
        total = nota // total_avaliacoes
        media = {
            'full': range(total),
            'empty': range((5 - total)),
            'nota1': nota1,
            'nota2': nota2,
            'nota3': nota3,
            'nota4': nota4,
            'nota5': nota5,
            'pb1': int(nota1 / total_avaliacoes * 100),
            'pb2': int(nota2 / total_avaliacoes * 100),
            'pb3': int(nota3 / total_avaliacoes * 100),
            'pb4': int(nota4 / total_avaliacoes * 100),
            'pb5': int(nota5 / total_avaliacoes * 100),
        }

        context['media'] = media
        return context

    def get_queryset(self):
        return Prestador.objects.get(pk=self.kwargs['pk'])
