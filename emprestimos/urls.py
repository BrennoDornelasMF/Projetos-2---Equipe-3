from django.urls import path

from .views import (
    solicitar_emprestimo,
    painel_emprestimos,
    aceitar_emprestimo,
    devolver_livro
)

urlpatterns = [

    path(
        'solicitar/<int:livro_id>/',
        solicitar_emprestimo,
        name='solicitar_emprestimo'
    ),

    path(
        'painel/<int:biblioteca_id>/',
        painel_emprestimos,
        name='painel_emprestimos'
    ),

    path(
        'aceitar/<int:id>/',
        aceitar_emprestimo,
        name='aceitar_emprestimo'
    ),

    path(
        'devolver/<int:id>/',
        devolver_livro,
        name='devolver_livro'
    ),
]