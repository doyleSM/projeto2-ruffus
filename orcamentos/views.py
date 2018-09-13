from django.views.generic import CreateView, ListView
from .models import Solicitacao, Orcamento
from catalogo.models import Servico
from usuarios.models import Cliente, Categoria
from .forms import SolicitacaoForm, OrcamentoForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
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
        #form.instance.cliente = Cliente.objects.get(user=self.request.user)
        #form.instance.servico = Servico.objects.get(slug=self.kwargs['slug'])
        form.save()

        return redirect(self.get_success_url())

    #def get_context_data(self, **kwargs):
    #    context = super(SolicitacaoView, self).get_context_data(**kwargs)
    #    context['servico'] = Servico.objects.get(slug=self.kwargs['slug'])
    #    return context

    def get_success_url(self):
        messages.success(self.request, 'Orçamento enviado com sucesso!')
        return reverse('index')


@method_decorator([login_required(login_url='usuarios:login'), prestador_required(login_url='usuarios:login')], name='dispatch')
class SolicitacoesAbertasListView(ListView):

    template_name = 'orcamentos/solicitacoes_prestador.html'
    context_object_name = 'solicitacoes'

    def get_queryset(self):

        prestador = self.request.user.prestador
        categorias = Categoria.objects.filter(prestador=prestador)

        return Solicitacao.objects.filter(servico__categoria__in=categorias)
