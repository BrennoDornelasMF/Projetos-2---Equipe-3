from django.urls import path

from .views import (
    criar_biblioteca,
    painel_bibliotecario,
    detalhes_biblioteca
)

urlpatterns = [

    path(
        'painel/',
        painel_bibliotecario,
        name='painel_bibliotecario'
    ),

    path(
        'criar/',
        criar_biblioteca,
        name='criar_biblioteca'
    ),

    path(
    '<int:id>/',
    detalhes_biblioteca,
    name='detalhes_biblioteca'
    ),
]