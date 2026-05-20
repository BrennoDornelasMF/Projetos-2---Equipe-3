from django.urls import path

from .views import adicionar_livro


urlpatterns = [

    path(
        'adicionar/<int:biblioteca_id>/',
        adicionar_livro,
        name='adicionar_livro'
    ),
]