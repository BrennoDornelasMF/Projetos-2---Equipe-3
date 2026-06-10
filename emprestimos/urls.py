from django.urls import path

from .views import (
    solicitar_emprestimo,
    painel_emprestimos,
    aceitar_emprestimo,
    devolver_livro,
    devolver_emprestimo,
    registrar_doacao,
    ativar_aviso,
    meus_avisos,
    listar_sugestoes,
    sugerir_titulo,
    votar_sugestao,
    gerenciar_sugestao,
    listar_desafios,
    participar_desafio,
    criar_desafio,
    leitores_ativos,
)

urlpatterns = [

    path('solicitar/<int:livro_id>/', solicitar_emprestimo, name='solicitar_emprestimo'),
    path('painel/<int:biblioteca_id>/', painel_emprestimos, name='painel_emprestimos'),
    path('aceitar/<int:id>/', aceitar_emprestimo, name='aceitar_emprestimo'),
    path('devolver/<int:emprestimo_id>/', devolver_livro, name='devolver_livro'),
    path('devolver-emp/<int:id>/', devolver_emprestimo, name='devolver_emprestimo'),
    path('doacao/<int:biblioteca_id>/', registrar_doacao, name='registrar_doacao'),
    path('leitores/<int:biblioteca_id>/', leitores_ativos, name='leitores_ativos'),

    path('avisos/ativar/<int:livro_id>/', ativar_aviso, name='ativar_aviso'),
    path('avisos/', meus_avisos, name='meus_avisos'),

    path('sugestoes/', listar_sugestoes, name='listar_sugestoes'),
    path('sugestoes/nova/', sugerir_titulo, name='sugerir_titulo'),
    path('sugestoes/votar/<int:sugestao_id>/', votar_sugestao, name='votar_sugestao'),
    path('sugestoes/gerenciar/<int:sugestao_id>/', gerenciar_sugestao, name='gerenciar_sugestao'),

    path('desafios/', listar_desafios, name='listar_desafios'),
    path('desafios/participar/<int:desafio_id>/', participar_desafio, name='participar_desafio'),
    path('desafios/criar/<int:biblioteca_id>/', criar_desafio, name='criar_desafio'),
]