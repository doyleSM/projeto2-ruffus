from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import ClienteCadastroForm, PrestadorCadastroForm, EnderecoForm, PrestadorCategoriasForm
from .models import User, Endereco, Prestador
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView


class ClienteCadastroView(CreateView):
    model = User
    form_class = ClienteCadastroForm
    template_name = 'usuarios/cadastro_cliente_form.html'


    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'cliente'
        return super().get_context_data(**kwargs)


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Usuario cadastrado com sucesso!')
        return reverse('index')


class PrestadorCadastroView(CreateView):
    model = User
    form_class = PrestadorCadastroForm
    template_name = 'usuarios/cadastro_prestador_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'prestador'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.warning(self.request, 'Cadastro realizado com sucesso! Usuário aguardando análise')
        return reverse('index')


@method_decorator(login_required, name='dispatch')
class EnderecoView(CreateView):
    model = Endereco
    form_class = EnderecoForm
    template_name = 'usuarios/cadastro_endereco_form.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(EnderecoView, self).form_valid(form)


def logout_view(request):
    logout(request)
    messages.success(request, 'Desconectado com sucesso!')
    return redirect('index')


class Login(LoginView):

    form_class = AuthenticationForm
    authentication_form = None
    #redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = 'index'

    def get_success_url(self):
        messages.success(self.request, 'Usuário logado')
        return reverse('index')

class PrestadorCategoriasView(UpdateView):
    model = Prestador
    form_class = PrestadorCategoriasForm
    template_name = 'usuarios/prestador_categorias_form.html'
    success_url = reverse_lazy('index')

    def get_object(self):
        return self.request.user.prestador

    def form_valid(self, form):
        messages.success(self.request, 'Categorias atualizadas com sucesso!')
        return super().form_valid(form)
