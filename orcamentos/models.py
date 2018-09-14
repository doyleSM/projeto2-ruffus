from django.db import models
from usuarios.models import Cliente, Endereco, Prestador
from catalogo.models import Servico
# Create your models here.


class Solicitacao(models.Model):

    cliente = models.ForeignKey('usuarios.Cliente', related_name='Cliente', on_delete=models.CASCADE)
    servico = models.ForeignKey('catalogo.Servico', on_delete=models.CASCADE)
    aberta = models.BooleanField('Aberta', default=True)
    endereco = models.ForeignKey('usuarios.Endereco', verbose_name='Endereço',on_delete=models.CASCADE)
    descricao = models.TextField('Descricao')
    hora_solicitacao = models.DateTimeField(auto_now_add=True)
    hora_aceitacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.servico.nome

    class Meta:
        verbose_name_plural = 'Solicitações'
        verbose_name = 'Solicitação'


class Orcamento(models.Model):

    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE)
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)
    aceito = models.BooleanField(default=False)
    descricao = models.TextField('Descrição')
    valor = models.DecimalField('Valor', decimal_places=2, max_digits=10)

    def __str__(self):
        return self.prestador.user.get_full_name() + ' - ' + str(self.valor)

    class Meta:
        verbose_name_plural = 'Orçamentos'
        verbose_name = 'Orçamento'
