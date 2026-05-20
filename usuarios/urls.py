from django.urls import path

from .views import cadastro, entrar, painel, sair

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', entrar, name='login'),
    path('painel/', painel, name='painel'),
    path('logout/', sair, name='logout'),
]