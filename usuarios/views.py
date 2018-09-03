from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, TemplateView, FormView, ListView, DeleteView
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


class MinhaContaClienteView(TemplateView):
    template_name = 'usuarios/minha_conta_cliente.html'


class AlterarSenhaView(FormView):
    template_name = 'usuarios/alterar_senha.html'
    #success_url = reverse_lazy('usuarios:cliente_conta')
    form_class = PasswordChangeForm

    def get_form_kwargs(self):
        kwargs = super(AlterarSenhaView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Senha alterada com sucesso!')
        return reverse('usuarios:cliente_conta')


class EnderecoView(CreateView):
    model = Endereco
    form_class = EnderecoForm
    template_name = 'usuarios/cadastro_endereco.html'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Endereco cadastrado com sucesso')
        return reverse('usuarios:lista_enderecos')


class EnderecoListView(ListView):
    template_name = 'usuarios/lista_endereco.html'
    context_object_name = 'enderecos'

    #paginate_by = 5

    def get_queryset(self):
        return Endereco.objects.filter(usuario=self.request.user)


class EnderecoEditar(UpdateView):
    model = Endereco
    form_class = EnderecoForm
    template_name = 'usuarios/cadastro_endereco.html'
    success_url = reverse_lazy('usuarios:lista_enderecos')

    def get_object(self):
        #return Endereco.objects.get(pk=self.kwargs['pk'], usuario=self.request.user)
        return get_object_or_404(Endereco, pk=self.kwargs['pk'], usuario=self.request.user)

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Endereco atualizado com sucesso')
        return reverse('usuarios:lista_enderecos')


class EnderecoDeletar(DeleteView):
    template_name_suffix = '_confirma_exclusao'
    model = Endereco

    def get_object(self):
        return get_object_or_404(Endereco, pk=self.kwargs['pk'], usuario=self.request.user)

    def get_success_url(self):
        messages.warning(self.request, 'Endereco removido com sucesso')
        return reverse('usuarios:lista_enderecos')