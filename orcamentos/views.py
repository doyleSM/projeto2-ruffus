from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .models import Solicitacao, Orcamento
from catalogo.models import Servico
from usuarios.models import Cliente, Categoria, Prestador
from .forms import SolicitacaoForm, OrcamentoForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from usuarios.decorators import cliente_required, prestador_required
# Create your views here.


@method_decorator([login_required(login_url='usuarios:login'), cliente_required(login_url='usuarios:login')], name='dispatch')
class SolicitacaoView(CreateView):

    model = Solicitacao
    form_class = SolicitacaoForm
    template_name = 'orcamentos/nova_solicitacao.html'

    def form_valid(self, form):
        form.instance.cliente = Cliente.objects.get(user=self.request.user)
        form.instance.servico = Servico.objects.get(slug=self.kwargs['slug'])
        form.save()

        return redirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super(SolicitacaoView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SolicitacaoView, self).get_context_data(**kwargs)
        context['servico'] = Servico.objects.get(slug=self.kwargs['slug'])

        return context

    def get_success_url(self):
        messages.success(self.request, 'Solicitado com sucesso!')
        return reverse('usuarios:solicitacoes_cliente')


@method_decorator([login_required(login_url='usuarios:login'), cliente_required(login_url='usuarios:login')], name='dispatch')
class SolicitacaoListView(ListView):
    template_name = 'orcamentos/minhas_solicitacoes.html'
    context_object_name = 'solicitacoes'

    def get_queryset(self):
        return Solicitacao.objects.filter(cliente_id=self.request.user.cliente.pk)


@method_decorator([login_required(login_url='usuarios:login'), prestador_required(login_url='usuarios:login')], name='dispatch')
class OrcamentoView(CreateView):

    model = Orcamento
    form_class = OrcamentoForm
    template_name = 'orcamentos/novo_orcamento.html'

    def form_valid(self, form):
        form.instance.prestador = Prestador.objects.get(user=self.request.user.prestador)
        form.instance.solicitacao = Solicitacao.objects.get(pk=self.kwargs['pk'])
        form.save()

        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(OrcamentoView, self).get_context_data(**kwargs)
        context['solicitacao'] = Solicitacao.objects.get(pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        messages.success(self.request, 'Orçamento enviado com sucesso!')
        return reverse('orcamentos:orcamentos-dados')


@method_decorator([login_required(login_url='usuarios:login'), prestador_required(login_url='usuarios:login')], name='dispatch')
class SolicitacoesAbertasListView(ListView):

    template_name = 'orcamentos/solicitacoes_prestador.html'
    context_object_name = 'solicitacoes'

    def get_queryset(self):

        prestador = self.request.user.prestador
        categorias = Categoria.objects.filter(prestador=prestador)

        return Solicitacao.objects.filter(servico__categoria__in=categorias, status=0)


@method_decorator([cliente_required(login_url='usuarios:login')], name='dispatch')
class OrcamentosListViewSolicitacoes(ListView):
    template_name = 'orcamentos/orcamentos_solicitacao.html'
    context_object_name = 'orcamentos'

    def get_context_data(self, **kwargs):
        context = super(OrcamentosListViewSolicitacoes, self).get_context_data(**kwargs)
        solicitacao = Solicitacao.objects.get(id=self.kwargs['pk'])

        context['servico'] = solicitacao.servico
        return context

    def get_queryset(self):
        return Orcamento.objects.filter(solicitacao_id=self.kwargs['pk'])


@cliente_required(login_url='usuarios:login')
def aceitarOrcamento(request, orcamentopk, solicitacaopk):

        orcamento = Orcamento.objects.get(pk=orcamentopk)
        solicitacao = Solicitacao.objects.get(pk=solicitacaopk)
        if solicitacao.cliente.user != request.user:
            messages.error(request, 'Você não tem permissão!')
            return redirect('index')
        else:
            if solicitacao.status != 0:
                messages.warning(request, 'Você já aceitou um orçamento para essa solicitação')
                return redirect('orcamentos:orcamentos_solicitacoes', solicitacaopk)
            else:
                solicitacao.status = 1
                solicitacao.orcamento_aceito = orcamento
                solicitacao.save()
                messages.success(request, 'Orçamento aceito com sucesso!')
                return redirect('orcamentos:orcamentos_solicitacoes', solicitacaopk)


@cliente_required(login_url='usuarios:login')
def cancelarSolicitacao(request, solicitacaopk):
    solicitacao = Solicitacao.objects.get(pk=solicitacaopk)
    if solicitacao.cliente.user != request.user:
        messages.error(request, 'Você não tem permissão!')
        return redirect('index')
    else:
        if solicitacao.status != 0:
            messages.error(request, 'Você já aceitou um orçamento, não há mais possibilidade de cancelamento')
            messages.warning(request, 'Em paralelo estamos trabalhando para melhorar as opções de cancelamento, agradecemos a compreensão')
            return redirect('usuarios:solicitacoes_cliente')
        else:
            solicitacao.status = 2
            solicitacao.save()
            messages.success(request, 'Solicitacção cancelada com sucesso!')
            return redirect('usuarios:solicitacoes_cliente')


@cliente_required(login_url='usuarios:login')
def descartarOrcamento(request, orcamentopk):
    orcamento = Orcamento.objects.get(pk=orcamentopk)
    if orcamento.solicitacao.cliente != request.user.cliente:
        messages.error(request, 'Você não tem permissão!')
        return redirect('index')
    else:
        if orcamento.descartar == 1:
            messages.warning(request, 'Orçamento já descartado')
            return redirect('orcamentos:orcamentos_solicitacoes', orcamento.solicitacao.pk)
        else:
            orcamento.descartar = 1
            orcamento.save()
            messages.success(request, 'Orçamento descartado com sucesso')
            return redirect('orcamentos:orcamentos_solicitacoes', orcamento.solicitacao.pk)


@cliente_required(login_url='usuarios:login')
def restaurarOrcamento(request, orcamentopk):
    orcamento = Orcamento.objects.get(pk=orcamentopk)
    if orcamento.solicitacao.cliente != request.user.cliente:
        messages.error(request, 'Você não tem permissão!')
        return redirect('index')
    else:
        if orcamento.descartar == 0:
            messages.warning(request, 'Orçamento já ativo')
            return redirect('orcamentos:orcamentos_solicitacoes', orcamento.solicitacao.pk)
        else:
            orcamento.descartar = 0
            orcamento.save()
            messages.success(request, 'Orçamento restaurado com sucesso')
            return redirect('orcamentos:orcamentos_solicitacoes', orcamento.solicitacao.pk)


@method_decorator([prestador_required(login_url='usuarios:login')], name='dispatch')
class OrcamentosPrestador(ListView):
    template_name = 'orcamentos/orcamentos_dados.html'
    context_object_name = 'orcamentos'

    def get_queryset(self):
        return Orcamento.objects.filter(prestador=self.request.user.prestador).order_by('solicitacao__servico__nome')


@prestador_required(login_url='usuarios:login')
def cancelarOrcamento(request, orcamentopk):
    orcamento = Orcamento.objects.get(pk=orcamentopk)
    try:
        solicitacao = Solicitacao.objects.get(orcamento_aceito=orcamento)
    except Solicitacao.DoesNotExist:
        solicitacao = None

    if orcamento.prestador != request.user.prestador:
        messages.error(request, 'Você não tem permissão!')
        return redirect('index')

    if solicitacao is None:
        messages.success(request, 'Orcamento cancelado com sucesso')
        orcamento.delete()
        return redirect('orcamentos:orcamentos-dados')

    if solicitacao.status != 0:
        messages.error(request, 'Orçamento já foi aceito, não há mais possibilidade de cancelamento')
        messages.warning(request, 'Em paralelo estamos trabalhando para melhorar as opções de cancelamento, agradecemos a compreensão')
        return redirect('orcamentos:orcamentos-dados')
    else:
        solicitacao.status = 3
        solicitacao.save()
        messages.success(request, 'orcamento cancelada com sucesso!')
        return redirect('orcamentos:orcamentos-dados')


@prestador_required(login_url='usuarios:login')
def confimarRealizacao(request, orcamentopk):
    orcamento = Orcamento.objects.get(pk=orcamentopk)
    try:
        solicitacao = Solicitacao.objects.get(orcamento_aceito=orcamento)
    except Solicitacao.DoesNotExist:
        solicitacao = None

    if orcamento.prestador != request.user.prestador:
        messages.error(request, 'Você não tem permissão!')
        return redirect('index')

    if solicitacao is None:
        messages.warning(request, 'Ocorreu um erro, tente novamente mais tarde')
        return redirect('orcamentos:orcamentos-dados')

    if solicitacao.status != 1:
        messages.error(request, 'Não é possível confirmar a realização do serviço')
        return redirect('orcamentos:orcamentos-dados')
    else:
        solicitacao.status = 4
        solicitacao.save()
        messages.success(request, 'solicitacao atulizada com sucesso!')
        return redirect('orcamentos:orcamentos-dados')