from usuarios.models import Prestador
from django.views.generic import ListView
from orcamentos.models import Solicitacao, Orcamento
# Create your views here.

class PerfilPrestador(ListView):

    template_name = 'perfis/perfil_prestador.html'
    context_object_name = 'perfil'

    #paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super(PerfilPrestador, self).get_context_data(**kwargs)
        context['completos'] = Solicitacao.objects.filter(status=5, orcamento_aceito__prestador=self.kwargs['pk']).count()
        return context

    def get_queryset(self):
        return Prestador.objects.get(pk=self.kwargs['pk'])

