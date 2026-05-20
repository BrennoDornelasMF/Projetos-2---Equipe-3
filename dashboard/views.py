from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth.decorators import login_required

from bibliotecas.models import Biblioteca
from livros.models import Livro
from emprestimos.models import Emprestimo


@login_required
def dashboard(request):

    user = request.user

    # =========================
    # BIBLIOTECÁRIO
    # =========================

    if user.tipo_usuario == 'bibliotecario':

        bibliotecas = Biblioteca.objects.filter(
            criado_por=user
        )

        livros = Livro.objects.filter(
            biblioteca__criado_por=user
        )

        emprestimos_ativos = Emprestimo.objects.filter(
            biblioteca__criado_por=user,
            status='emprestado'
        )

        emprestimos_pendentes = Emprestimo.objects.filter(
            biblioteca__criado_por=user,
            status='pendente'
        )

        context = {

            'tipo': 'bibliotecario',

            'total_bibliotecas':
                bibliotecas.count(),

            'total_livros':
                livros.count(),

            'emprestimos_ativos':
                emprestimos_ativos.count(),

            'emprestimos_pendentes':
                emprestimos_pendentes.count(),

            'bibliotecas':
                bibliotecas
        }

        return render(
            request,
            'dashboard/bibliotecario.html',
            context
        )

    # =========================
    # LEITOR
    # =========================

    emprestimos = Emprestimo.objects.filter(
        leitor=user
    ).order_by('-data_emprestimo')

    emprestados = emprestimos.filter(
        status='emprestado'
    )

    pendentes = emprestimos.filter(
        status='pendente'
    )

    context = {

        'tipo': 'leitor',

        'emprestimos': emprestimos,

        'emprestados': emprestados,

        'pendentes': pendentes,
    }

    return render(
        request,
        'dashboard/leitor.html',
        context
    )