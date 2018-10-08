from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from usuarios.models import Cliente, Endereco, User, Prestador


class ClienteCadastroForm(UserCreationForm):
    CPF = forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'CPF')

    @transaction.atomic
    def save(self, cpf):
        user = super().save(commit=False)
        user.is_cliente = True
        user.save()
        Cliente.objects.create(user=user)
        user.cliente.CPF = cpf
        user.cliente.save()
        return user


class PrestadorCadastroForm(UserCreationForm):
    CPF = forms.CharField()
    telefone = forms.CharField()
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'CPF')

    @transaction.atomic
    def save(self, cpf, telefone):
        user = super().save(commit=False)

        user.is_prestador = True
        user.is_active = True
        user.save()
        Prestador.objects.create(user=user)
        user.prestador.CPF = cpf
        user.prestador.telefone = telefone
        user.prestador.save()

        return user


class PrestadorCategoriasForm(ModelForm):
    class Meta:
        model = Prestador
        fields = ('categorias', )
        widgets = {
            'categorias': CheckboxSelectMultiple
        }


class EnderecoForm(ModelForm):

    class Meta:

        model = Endereco
        fields = ['nome_rua', 'complemento', 'bairro', 'CEP', ]