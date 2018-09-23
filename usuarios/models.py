from django.contrib.auth.models import AbstractUser
from django.db import models
from catalogo.models import Categoria


class User(AbstractUser):

    is_cliente = models.BooleanField(default=False)
    is_prestador = models.BooleanField(default=False)


class Endereco(models.Model):

    nome_rua = models.CharField('Rua', max_length=50 )
    complemento = models.CharField('Complemento', max_length=30, null=True, blank=True)
    bairro = models.CharField('Bairro', max_length=50)
    CEP = models.CharField('CEP', max_length=15)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome_rua + ' ' + self.complemento + ' ' + self.bairro


class Cliente(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    CPF = models.CharField('CPF', max_length=15)

    def __str__(self):
        return self.user.username


class Prestador(models.Model):

    data_cadastro = models.DateField('Ingressou em', auto_now_add=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    CPF = models.CharField('CPF', max_length=15, default='12345678')
    categorias = models.ManyToManyField(Categoria, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Prestadores'
        verbose_name = 'Prestador'

    def get_categorias(self):
        categorias = Categoria.objects.filter(prestador=self)
        return categorias