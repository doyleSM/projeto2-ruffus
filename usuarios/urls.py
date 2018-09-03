from django.urls import path
from .views import ClienteCadastroView, logout_view, PrestadorCadastroView, PrestadorCategoriasView, Login, MinhaContaClienteView
from .views import AlterarSenhaView, EnderecoView, EnderecoListView, EnderecoEditar, EnderecoDeletar, DadosPessoaisList

app_name = 'usuarios'
urlpatterns = [
    path('cadastro/cliente/', ClienteCadastroView.as_view(), name='cadastro_cliente'),
    path('cadastro/prestador/', PrestadorCadastroView.as_view(), name='cadastro_prestador'),
    path('cadastro/categorias/', PrestadorCategoriasView.as_view(), name='categorias_prestador'),
    path('cadastro/endereco/', EnderecoView.as_view(), name='cadastro_endereco'),
    path('enderecos/', EnderecoListView.as_view(), name='lista_enderecos'),
    path('minha-conta/', MinhaContaClienteView.as_view(), name='cliente_conta'),
    path('alterar-senha/', AlterarSenhaView.as_view(), name='alterar_senha'),
    path('endereco/atualizar/<int:pk>/', EnderecoEditar.as_view(), name='editar_endereco'),
    path('endereco/deletar/<int:pk>/', EnderecoDeletar.as_view(), name='deletar_endereco'),
    path('dados-pessoais/', DadosPessoaisList.as_view(), name='dados_pessoais'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
