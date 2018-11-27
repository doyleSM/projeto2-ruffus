from django.contrib import admin
from .models import Cliente, User, Endereco, Prestador


class ClienteAdmin(admin.ModelAdmin):
    fields = [('CPF', 'user', 'telefone'), ]
    list_display = ['usuario', 'nome', 'CPF', 'status', 'endereco', 'telefone']
    search_fields = ['nome',]

    def nome(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def usuario(self, obj):
        return obj.user.username

    def status(self, obj):
        if obj.user.is_active:
            return 'Ativo'
        return 'Inativo'

    def endereco(self, obj):
        usuario = User.objects.get(pk=obj.user.pk)
        enderecos = Endereco.objects.filter(usuario=usuario)
        endereco = ''
        for end in enderecos:
            endereco += end.nome_rua + ' - '
        return endereco


class EnderecoAdmin(admin.ModelAdmin):
    list_display = ['nome_rua', 'complemento', 'bairro', 'CEP', 'usuario']
    search_fields = ['nome_rua',]
    autocomplete_fields = ('usuario',)


class UserAdmin(admin.ModelAdmin):
    search_fields = ['nome',]


class PrestadorAdmin(admin.ModelAdmin):
    fields = [('CPF', 'user', 'telefone'), 'categorias' ]
    list_display = ['pk', 'usuario', 'nome', 'CPF', 'status', 'endereco', 'telefone']
    search_fields = ['nome']

    def nome(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def usuario(self, obj):
        return obj.user.username

    def status(self, obj):
        if(obj.user.is_active):
            return 'Ativo'
        return 'Inativo'

    def endereco(self, obj):
        usuario = User.objects.get(pk=obj.user.pk)
        enderecos = Endereco.objects.filter(usuario=usuario)
        endereco = ''
        for end in enderecos:
            endereco += end.nome_rua + ' - '
        return endereco


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Endereco, EnderecoAdmin)
admin.site.register(Prestador, PrestadorAdmin)