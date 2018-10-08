from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from .models import Avaliacao
from usuarios.models import Cliente, Prestador
from orcamentos.models import Orcamento
from .forms import AvaliacaoForm
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse
# Create your views here.
from usuarios.decorators import cliente_required, prestador_required


@method_decorator([cliente_required(login_url='usuarios:login')], name='dispatch')
class AvaliacaoView(CreateView):

    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'avaliacoes/nova_avaliacao.html'

    def form_valid(self, form):
        orcamento = Orcamento.objects.get(pk=self.kwargs['orcamentopk'])

        if orcamento.solicitacao.cliente != self.request.user.cliente:
            messages.error(self.request, 'Você nao pode avaliar essa solicitacao')
            return redirect('index')

        if orcamento.solicitacao.status not in [3, 5]:
            messages.error(self.request, 'Orcamento só pode ser avaliado se a solicitacao estiver concluida ou cancelada pelo prestador')
            return redirect('usuarios:solicitacoes_cliente')

        if orcamento.solicitacao.avaliado:
            messages.warning(self.request, 'Serviço já avaliado')
            return redirect('perfis:prefil_prestador', orcamento.solicitacao.orcamento_aceito.prestador_id)

        form.instance.orcamento = orcamento
        form.instance.usuario = Cliente.objects.get(user=self.request.user)
        form.save()
        orcamento.solicitacao.avaliado = True
        orcamento.solicitacao.save()

        return self.get_success_url(orcamento.solicitacao.orcamento_aceito.prestador_id)

    def get_context_data(self, **kwargs):
        context = super(AvaliacaoView, self).get_context_data(**kwargs)
        orcamento = Orcamento.objects.get(pk=self.kwargs['orcamentopk'])
        context['solicitacao'] = orcamento.solicitacao
        return context

    def get_success_url(self, pk):
        messages.success(self.request, 'Avaliação feita com sucesso!')
        return redirect('perfis:prefil_prestador', pk)


@method_decorator([prestador_required(login_url='usuarios:login')], name='dispatch')
class AvaliacaoPeloPrestador(CreateView):

    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'avaliacoes/nova_avaliacao.html'

    def form_valid(self, form):
        orcamento = Orcamento.objects.get(pk=self.kwargs['orcamentopk'])

        if orcamento.solicitacao.orcamento_aceito.prestador != self.request.user.prestador:
            messages.error(self.request, 'Você nao pode avaliar esse usuário')
            return redirect('index')

        if orcamento.solicitacao.status not in [2, 5]:
            messages.error(self.request, 'Orcamento só pode ser avaliado se a solicitacao estiver concluida ou cancelada pelo cliente')
            return redirect('index')

        if orcamento.solicitacao.prestador_avaliou:
            messages.warning(self.request, 'Usuario já avaliado')
            return redirect('index')

        form.instance.orcamento = orcamento
        form.instance.usuario2 = Prestador.objects.get(user=self.request.user)
        form.instance.prestador_avaliou = True
        form.save()
        orcamento.solicitacao.prestador_avaliou = True
        orcamento.solicitacao.save()


        return self.get_success_url(orcamento.solicitacao.cliente_id)

    def get_context_data(self, **kwargs):
        context = super(AvaliacaoPeloPrestador, self).get_context_data(**kwargs)
        orcamento = Orcamento.objects.get(pk=self.kwargs['orcamentopk'])
        context['solicitacao'] = orcamento.solicitacao
        return context

    def get_success_url(self, pk):
        messages.success(self.request, 'Avaliação feita com sucesso!')
        return redirect('perfis:perfil_cliente', pk)
