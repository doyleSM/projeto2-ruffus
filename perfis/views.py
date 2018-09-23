from django.shortcuts import render
from usuarios.models import Prestador
from django.views.generic import ListView

# Create your views here.

class PerfilPrestador(ListView):

    template_name = 'perfis/perfil_prestador'
    context_object_name = 'perfil'

    #paginate_by = 5

    def get_queryset(self):
        return Prestador.objects.get(self.kwargs['pk'])