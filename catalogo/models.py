# -*- coding: utf 8 -*-


from django.db import models
from django.urls import reverse


# Create your models here.
class Categoria(models.Model):

    nome = models.CharField('Nome', max_length=50)
    slug = models.CharField('Identificador', max_length=50)
    data_criacao = models.DateTimeField('Criado em', auto_now_add=True)
    data_modificacao = models.DateTimeField('Modificado em', auto_now=True)

    class Meta:

        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('catalogo:lista_por_categoria', kwargs={'slug': self.slug})


class Servico(models.Model):

    nome = models.CharField('Nome', max_length=50)
    slug = models.CharField('Identificador', max_length=50)
    categoria = models.ForeignKey(Categoria, verbose_name='Categoria', on_delete=models.PROTECT)
    descricao = models.TextField('Descrição', blank=True)
    data_criacao = models.DateTimeField('Criado em', auto_now_add=True)
    data_modificacao = models.DateTimeField('Modificado em', auto_now=True)
    preco = models.DecimalField('Preço', decimal_places=2, max_digits=10)
    imagem = models.ImageField('Imagem', upload_to='servicos', blank=True, null=True)

    class Meta:

        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'
        ordering = ['nome']

    def __str__(self):
        return self.nome