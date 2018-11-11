from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from usuarios.models import Prestador, Cliente
from django.views.generic import ListView
from orcamentos.models import Solicitacao
from avaliacoes.models import Avaliacao
# Create your views here.

@method_decorator([login_required(login_url='usuarios:login')], name='dispatch')
class PerfilPrestador(ListView):

    template_name = 'perfis/perfil_prestador.html'
    context_object_name = 'perfil'

    #paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super(PerfilPrestador, self).get_context_data(**kwargs)
        context['completos'] = Solicitacao.objects.filter(status=4, orcamento_aceito__prestador=self.kwargs['pk']).count()
        context['avaliacoes'] = Avaliacao.objects.filter(orcamento__prestador=self.kwargs['pk'], prestador_avaliou=False)
        avaliacoes = Avaliacao.objects.filter(orcamento__prestador=self.kwargs['pk'], prestador_avaliou=False)
        nota1 = avaliacoes.filter(nota=1).count()
        nota2 = avaliacoes.filter(nota=2).count()
        nota3 = avaliacoes.filter(nota=3).count()
        nota4 = avaliacoes.filter(nota=4).count()
        nota5 = avaliacoes.filter(nota=5).count()
        nota = 0
        total = 0
        media_aval = 0

        total_avaliacoes = avaliacoes.count()
        if total_avaliacoes == 0:
            total_avaliacoes = 1

        for avaliacao in avaliacoes:
            nota += avaliacao.nota

            if nota > 0:
                total = nota // total_avaliacoes
                media_aval = nota / total_avaliacoes
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
            'media_aval': round(media_aval, 2)

        }

        context['media'] = media
        return context

    def get_queryset(self):
        return Prestador.objects.get(pk=self.kwargs['pk'])


@method_decorator([login_required(login_url='usuarios:login')], name='dispatch')
class PerfilCliente(ListView):

    template_name = 'perfis/perfil_cliente.html'
    context_object_name = 'perfil'

    #paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(PerfilCliente, self).get_context_data(**kwargs)
        cliente = Cliente.objects.get(pk=self.kwargs['pk'])
        context['contratados'] = Solicitacao.objects.filter(status=4, cliente=cliente).count()
        context['avaliacoes'] = Avaliacao.objects.filter(orcamento__solicitacao__cliente=cliente, prestador_avaliou=True)
        avaliacoes = Avaliacao.objects.filter(orcamento__solicitacao__cliente=cliente, prestador_avaliou=True)
        nota1 = avaliacoes.filter(nota=1).count()
        nota2 = avaliacoes.filter(nota=2).count()
        nota3 = avaliacoes.filter(nota=3).count()
        nota4 = avaliacoes.filter(nota=4).count()
        nota5 = avaliacoes.filter(nota=5).count()
        nota = 0
        total = 0
        media_aval = 0

        total_avaliacoes = avaliacoes.count()
        if total_avaliacoes == 0:
            total_avaliacoes = 1

        for avaliacao in avaliacoes:
            nota += avaliacao.nota

            if nota > 0:
                total = nota // total_avaliacoes
                media_aval = nota / total_avaliacoes
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
            'media_aval': round(media_aval)
        }

        context['media'] = media
        return context

    def get_queryset(self):
        return Cliente.objects.get(pk=self.kwargs['pk'])