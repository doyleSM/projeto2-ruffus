from django.contrib import admin
from .models import Cliente, User, Endereco

class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'usuario', 'CPF', 'status', 'endereco']
    #search_fields = ['nome', 'slug']

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
        endereco = Endereco.objects.get(usuario=usuario)
        return endereco


# Register your models here.
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(User)
admin.site.register(Endereco)