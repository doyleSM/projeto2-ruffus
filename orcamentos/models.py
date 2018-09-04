from django.db import models
from usuarios.models import Cliente, Endereco
from catalogo.models import Servico
# Create your models here.

class Solicitacao(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.PROTECT)
    servico = models.OneToOneField(Servico, on_delete=models.PROTECT)
    aberta = models.BooleanField('Status', default=True)
    endereco = models.OneToOneField(Endereco, on_delete=models.PROTECT)
    descricao = models.TextField('Descricao')
    hora_solicitacao = models.DateTimeField(auto_now_add=True)
    hora_aceitacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Solicitacao teste'

    class Meta:
        verbose_name_plural = 'Solicitações'
        verbose_name = 'Solicitação'

