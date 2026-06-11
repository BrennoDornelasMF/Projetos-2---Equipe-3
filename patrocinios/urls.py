from django.urls import path
from .views import registrar_patrocinio, listar_patrocinios

urlpatterns = [

    path(
        'registrar/<int:biblioteca_id>/',
        registrar_patrocinio,
        name='registrar_patrocinio'
    ),

    path(
        'listar/<int:biblioteca_id>/',
        listar_patrocinios,
        name='listar_patrocinios'
    ),
]