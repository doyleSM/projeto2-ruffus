from django.shortcuts import render
from django.views.generic import CreateView
from .models import Solicitacao
from catalogo.models import Servico
from usuarios.models import Cliente
from .forms import SolicitacaoForm
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
# Create your views here.


class SolicitacaoView(CreateView):

    model = Solicitacao
    form_class = SolicitacaoForm
    template_name = 'orcamentos/nova_solicitacao.html'

    def form_valid(self, form):
        form.save()
        #form.instance.cliente = Cliente.objects.get(user=self.request.user)
        #form.instance.servico = Servico.objects.get(slug=self.kwargs['slug'])
        #form.instance.servico.set(Servico.objects.get(slug=self.kwargs['slug']))
        #form.instance.cliente.set(Cliente.objects.get(user=self.request.user))

        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Solicitado com sucesso!')
        return reverse('index')