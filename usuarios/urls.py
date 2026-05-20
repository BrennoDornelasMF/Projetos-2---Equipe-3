from django.urls import path

from .views import cadastro, entrar

urlpatterns = [
    path('cadastro/', cadastro, name='cadastro'),
    path('login/', entrar, name='login'),
]