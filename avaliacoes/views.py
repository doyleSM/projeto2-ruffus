from django.shortcuts import render, redirect
from .models import Avaliacao
from usuarios.models import Cliente
from orcamentos.models import Orcamento
from .forms import AvaliacaoForm
from django.views.generic import CreateView
from django.contrib import messages
from django.urls import reverse
# Create your views here.
class AvaliacaoView(CreateView):

    model = Avaliacao
    form_class = AvaliacaoForm
    template_name = 'orcamentos/novo_orcamento.html'

    def form_valid(self, form):
        orcamento = Orcamento.objects.get(pk=self.kwargs['orcamentopk'])

        if orcamento.solicitacao.cliente != self.request.user.cliente:
            messages.error(self.request, 'Você nao pode avaliar essa solicitacao')
            return redirect('index')

        if orcamento.solicitacao.status != 3 or orcamento.solicitacao.status != 5:
            messages.error(self.request, ('Orcamento só pode ser avaliado se a solicitacao estiver concluida ou cancelada pelo prestador'))
            return redirect('index')

        if orcamento.avaliado:
            messages.warning(self.request, 'Orçamento já avaliado')
            return redirect('index')

        form.instance.orcamento = orcamento
        form.instance.usuario = Cliente.objects.get(user=self.request.user)
        form.instance.avaliado = True
        form.save()

        return redirect(self.get_success_url())

    #def get_context_data(self, **kwargs):
    #    context = super(SolicitacaoView, self).get_context_data(**kwargs)
    #    context['servico'] = Servico.objects.get(slug=self.kwargs['slug'])
    #    return context

    def get_success_url(self):
        messages.success(self.request, 'Avaliação feita com sucesso!')
        return reverse('index')