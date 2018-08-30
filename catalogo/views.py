# -*- coding: utf 8 -*-


from django.shortcuts import get_object_or_404
from django.views import generic
from .models import Servico, Categoria
from django.http import JsonResponse

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


class DetalheServicoView(generic.ListView):

    template_name = 'catalogo/detalhe_servico.html'
    context_object_name = 'servico'

    def get_queryset(self):
        return Servico.objects.get(slug=self.kwargs['slug'])


detalhe_servico = DetalheServicoView.as_view()


def get_categorias(request):
    categorias = [
        dict(id=categoria.id, nome=categoria.nome, data_cria=categoria.data_criacao, data_mod=categoria.data_modificacao)
        for categoria in Categoria.objects.all()
    ]
    return JsonResponse(dict(categorias=categorias))