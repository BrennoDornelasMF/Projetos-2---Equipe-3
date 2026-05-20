from django.urls import path

from .views import cadastro, entrar, painel

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', entrar, name='login'),
    path('painel/', painel, name='painel'),
]