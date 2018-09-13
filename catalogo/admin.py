from django.contrib import admin
from .models import  Servico, Categoria

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['pk', 'nome', 'slug', 'data_criacao', 'data_modificacao']
    search_fields = ['nome', 'slug']

class ServicoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'categoria', 'descricao', 'preco', 'data_criacao', 'data_modificacao']
    search_fields = ['nome', 'slug', 'categoria__nome']


# Register your models here.
admin.site.register(Servico, ServicoAdmin)
admin.site.register(Categoria, CategoriaAdmin)