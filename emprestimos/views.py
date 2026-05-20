from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from datetime import timedelta

from django.utils import timezone

from django.contrib.auth.decorators import login_required

from .models import Emprestimo

from livros.models import Livro
from bibliotecas.models import Biblioteca

@login_required
def devolver_emprestimo(request, id):

    emprestimo = get_object_or_404(
        Emprestimo,
        id=id
    )

    if request.user != emprestimo.biblioteca.criado_por:

        return redirect('index')

    emprestimo.status = 'devolvido'

    emprestimo.save()

    livro = emprestimo.livro

    livro.quantidade += 1

    livro.disponivel = True

    livro.save()

    return redirect(
        'painel_emprestimos',
        emprestimo.biblioteca.id
    )


@login_required
def solicitar_emprestimo(request, livro_id):

    livro = get_object_or_404(
        Livro,
        id=livro_id
    )

    if request.user.tipo_usuario != 'leitor':
        return redirect('index')

    if livro.quantidade <= 0:
        return redirect('index')

    Emprestimo.objects.create(

        leitor=request.user,

        livro=livro,

        biblioteca=livro.biblioteca
    )

    return redirect('index')


@login_required
def painel_emprestimos(request, biblioteca_id):

    biblioteca = get_object_or_404(
        Biblioteca,
        id=biblioteca_id
    )

    if biblioteca.criado_por != request.user:
        return redirect('index')

    emprestimos = Emprestimo.objects.filter(
        biblioteca=biblioteca
    ).order_by('-data_emprestimo')

    return render(
        request,
        'emprestimos/painel.html',
        {
            'biblioteca': biblioteca,
            'emprestimos': emprestimos
        }
    )


@login_required
def aceitar_emprestimo(request, id):

    emprestimo = get_object_or_404(
        Emprestimo,
        id=id
    )

    if request.user != emprestimo.biblioteca.criado_por:

        return redirect('index')

    if request.method == 'POST':

        dias = int(
            request.POST.get('dias')
        )

        data_devolucao = (
            timezone.now().date()
            + timedelta(days=dias)
        )

        emprestimo.status = 'emprestado'

        emprestimo.data_devolucao = (
            data_devolucao
        )

        emprestimo.save()

        livro = emprestimo.livro

        livro.quantidade -= 1

        if livro.quantidade <= 0:

            livro.disponivel = False

        livro.save()

        return redirect(
            'painel_emprestimos',
            emprestimo.biblioteca.id
        )

    return render(
        request,
        'emprestimos/aceitar.html',
        {
            'emprestimo': emprestimo
        }
    )


@login_required
def devolver_livro(request, emprestimo_id):

    emprestimo = get_object_or_404(
        Emprestimo,
        id=emprestimo_id
    )

    if emprestimo.biblioteca.criado_por != request.user:
        return redirect('index')

    emprestimo.status = 'devolvido'

    emprestimo.save()

    livro = emprestimo.livro

    livro.quantidade += 1

    livro.disponivel = True

    livro.save()

    return redirect(
        'painel_emprestimos',
        biblioteca_id=emprestimo.biblioteca.id
    )