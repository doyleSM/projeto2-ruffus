from django.db import models
from orcamentos.models import Orcamento
from usuarios.models import Cliente
# Create your models here.


class Avaliacao(models.Model):
    NOTA_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE)
    data_pub = models.DateField('data publicação', auto_now_add=True)
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    comentario = models.CharField(max_length=200)
    nota = models.IntegerField(choices=NOTA_CHOICES)

    def __str__(self):
        return self.orcamento.prestador.user.get_full_name() + ' - ' + str(self.nota)

    class Meta:
        verbose_name = 'Avaliação'
        verbose_name_plural = 'Avaliações'