from django.urls import path

from .views import (
    adicionar_livro,
    editar_livro,
    excluir_livro
)

urlpatterns = [

    path(
        'adicionar/<int:biblioteca_id>/',
        adicionar_livro,
        name='adicionar_livro'
    ),

    path(
        'editar/<int:livro_id>/',
        editar_livro,
        name='editar_livro'
    ),

    path(
        'excluir/<int:livro_id>/',
        excluir_livro,
        name='excluir_livro'
    ),
]