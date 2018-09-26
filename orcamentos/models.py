from django.db import models
from usuarios.models import Cliente, Endereco, Prestador
from catalogo.models import Servico
# Create your models here.


class Solicitacao(models.Model):

    SOLICITACAO_STATUS = (
        (0, 'Solicitado'),
        (1, 'Aguardando prestador'),
        (2, 'Cancelado pelo cliente'),
        (3, 'Cancelado pelo prestador'),
        (4, 'Aguardando pagamento'),
        (5, 'Concluido')
    )

    cliente = models.ForeignKey('usuarios.Cliente', related_name='Cliente', on_delete=models.CASCADE)
    servico = models.ForeignKey('catalogo.Servico', on_delete=models.CASCADE)
    status = models.IntegerField('Status', choices=SOLICITACAO_STATUS, default=0)
    endereco = models.ForeignKey('usuarios.Endereco', verbose_name='Endereço', on_delete=models.CASCADE)
    descricao = models.TextField('Descricao')
    hora_solicitacao = models.DateTimeField(auto_now_add=True)
    hora_aceitacao = models.DateTimeField(auto_now=True)
    #orcamento_aceito = models.ForeignKey('orcamentos.Orcamento',related_name='orcamento_aceito', on_delete=models.CASCADE, null=True, blank=True)
    orcamento_aceito = models.OneToOneField('orcamentos.Orcamento',related_name='orcamento_aceito', on_delete=models.CASCADE, null=True, blank=True)
    avaliado = models.BooleanField(default=False)

    def __str__(self):
        return self.servico.nome

    def get_color(self):
        if self.status == 0:
            return 'green'
        elif self.status == 1:
            return 'blue'
        elif self.status == 2 or self.status == 3:
            return 'red'
        elif self.status == 4:
            return 'orange'
        else:
            return 'rgb(57,255,20)'

    def get_icon(self):
        if self.status == 0:
            return 'fa fa-clock-o'
        elif self.status == 1:
            return 'fa fa-hourglass-end'
        elif self.status == 2 or self.status == 3:
            return 'fa fa-exclamation-triangle'
        elif self.status == 4:
            return 'fa fa-credit-card'
        else:
            return 'fa fa-check-square'

    class Meta:
        verbose_name_plural = 'Solicitações'
        verbose_name = 'Solicitação'


class Orcamento(models.Model):

    prestador = models.ForeignKey(Prestador, on_delete=models.CASCADE)
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE)
    descartar = models.BooleanField(default=False)
    descricao = models.TextField('Descrição')
    valor = models.DecimalField('Valor', decimal_places=2, max_digits=10)

    def __str__(self):
        return self.prestador.user.get_full_name() + ' - ' + str(self.valor)

    class Meta:
        verbose_name_plural = 'Orçamentos'
        verbose_name = 'Orçamento'
