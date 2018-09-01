from django.contrib.auth import login
from django.shortcuts import redirect, render_to_response
from django.views.generic import CreateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .forms import ClienteCadastroForm, PrestadorCadastroForm, EnderecoForm
from .models import User, Endereco
from django.contrib import messages
from django.urls import  reverse
from django.contrib.auth import logout


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
        messages.warning(self.request, 'Prestador cadastrado com sucesso, aguarde análise')
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