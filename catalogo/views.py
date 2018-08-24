from django.shortcuts import render

# Create your views here.
from .models import Servico, Categoria


def lista_servicos(request):
    contexto = {
        'servicos': Servico.objects.all()
    }
    return render(request, 'catalogo/lista_servicos.html', contexto)


def lista_por_categoria(request, slug):

    categoria = Categoria.objects.get(slug=slug)
    contexto = {
        'categoria_atual': categoria,
        'servicos': Servico.objects.filter(categoria=categoria)
    }
    return render(request, 'catalogo/servicos_categoria.html', contexto)

def detalhe_servico(request, slug):

    servico = Servico.objects.get(slug=slug)
    contexto = {
        'servico': servico
    }
    return render(request, 'catalogo/detalhe_servico.html', contexto)