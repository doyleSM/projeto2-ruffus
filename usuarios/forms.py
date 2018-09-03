from django.forms import ModelForm, CheckboxSelectMultiple
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from usuarios.models import Cliente, Endereco, User, Prestador


class ClienteCadastroForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_cliente = True
        user.save()
        Cliente.objects.create(user=user)
        return user


class PrestadorCadastroForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_prestador = True
        user.is_active = False
        user.save()
        Prestador.objects.create(user=user)
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