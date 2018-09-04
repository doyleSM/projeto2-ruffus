from django.contrib import admin
from .models import Solicitacao, Orcamento

# Register your models here.

class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ['solicitacao', 'solicitante', 'servico', 'endereco', 'hora_solicitacao', 'aberta']

    def solicitante(self, obj):
        return obj.cliente.user.get_full_name()

    def solicitacao(self, obj):
        return obj.cliente.user.get_full_name() + ' - ' + obj.servico.nome


admin.site.register(Solicitacao, SolicitacaoAdmin)
admin.site.register(Orcamento)