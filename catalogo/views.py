# -*- coding: utf 8 -*-

from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from .models import Servico, Categoria
from usuarios.decorators import cliente_required


class ListaServicosView(generic.ListView):

    model = Servico
    template_name = 'catalogo/lista_servicos.html'
    context_object_name = 'servicos'


lista_servicos = ListaServicosView.as_view()


class ListaPorCategoriaView(generic.ListView):

    template_name = 'catalogo/servicos_categoria.html'
    context_object_name = 'servicos'

    def get_queryset(self):

        categoria = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return Servico.objects.filter(categoria=categoria)

    def get_context_data(self, **kwargs):
        context = super(ListaPorCategoriaView, self).get_context_data(**kwargs)
        context['categoria_atual'] = get_object_or_404(Categoria, slug=self.kwargs['slug'])
        return context


lista_por_categoria = ListaPorCategoriaView.as_view()


@method_decorator([cliente_required(login_url='usuarios:login')], name='dispatch')
class DetalheServicoView(generic.ListView):

    template_name = 'catalogo/detalhe_servico.html'
    context_object_name = 'servico'

    def get_queryset(self):
        return Servico.objects.get(slug=self.kwargs['slug'])


detalhe_servico = DetalheServicoView.as_view()

