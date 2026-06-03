from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from .models import Emprestimo, Doacao
from .forms import DoacaoForm
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

@login_required
def registrar_doacao(request, biblioteca_id):

    biblioteca = get_object_or_404(
        Biblioteca,
        id=biblioteca_id
    )

    if biblioteca.criado_por != request.user:
        return redirect('index')

    if request.method == 'POST':

        form = DoacaoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            titulo = form.cleaned_data['titulo']
            autor = form.cleaned_data['autor']
            categoria = form.cleaned_data['categoria']
            descricao = form.cleaned_data.get('descricao', '')
            capa = form.cleaned_data.get('capa')
            quantidade = form.cleaned_data['quantidade']
            nome_doador = form.cleaned_data['nome_doador']

            livro = Livro.objects.filter(
                titulo__iexact=titulo,
                biblioteca=biblioteca
            ).first()

            if livro:
                livro.quantidade += quantidade
                if livro.quantidade > 0:
                    livro.disponivel = True
                livro.save()

            else:
                livro = Livro.objects.create(
                    titulo=titulo,
                    autor=autor,
                    categoria=categoria,
                    descricao=descricao,
                    capa=capa,
                    quantidade=quantidade,
                    disponivel=True,
                    biblioteca=biblioteca
                )

            Doacao.objects.create(
                livro=livro,
                biblioteca=biblioteca,
                nome_doador=nome_doador,
                quantidade=quantidade
            )

            return redirect(
                'detalhes_biblioteca',
                id=biblioteca.id
            )

    else:

        form = DoacaoForm()

    return render(
        request,
        'emprestimos/doacao.html',
        {
            'form': form,
            'biblioteca': biblioteca
        }
    )