from django.db import models
from orcamentos.models import Orcamento
from usuarios.models import Cliente, Prestador
# Create your models here.


class Avaliacao(models.Model):
    NOTA_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    orcamento = models.OneToOneField(Orcamento, related_name='orcamento', on_delete=models.CASCADE)
    data_pub = models.DateField('data publicação', auto_now_add=True)
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    comentario = models.CharField(max_length=200)
    nota = models.IntegerField(choices=NOTA_CHOICES)
    usuario2 = models.ForeignKey(Prestador, on_delete=models.CASCADE, blank=True, null=True)
    prestador_avaliou = models.BooleanField(default=False)

    def __str__(self):
        try:
            return self.orcamento.prestador.user.get_full_name() + ' - ' + str(self.nota)
        except Exception:
            return self.orcamento.solicitacao.cliente.user.get_full_name() + ' - ' + str(self.nota)

    def star(self):
        avaliacao = {
            'full': range(self.nota),
            'empty': range(5-self.nota)
        }
        return avaliacao

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'