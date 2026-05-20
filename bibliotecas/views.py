from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from livros.models import Livro
from .forms import BibliotecaForm
from .models import Biblioteca

@login_required
def detalhes_biblioteca(request, id):

    biblioteca = get_object_or_404(
        Biblioteca,
        id=id
    )

    if biblioteca.criado_por != request.user:
        return redirect('index')

    livros = Livro.objects.filter(
        biblioteca=biblioteca
    )

    return render(
        request,
        'bibliotecas/detalhes.html',
        {
            'biblioteca': biblioteca,
            'livros': livros
        }
    )


@login_required
def painel_bibliotecario(request):

    if request.user.tipo_usuario != 'bibliotecario':
        return redirect('index')

    bibliotecas = Biblioteca.objects.filter(
        criado_por=request.user
    )

    return render(
        request,
        'bibliotecas/painel.html',
        {
            'bibliotecas': bibliotecas
        }
    )


@login_required
def criar_biblioteca(request):

    if request.user.tipo_usuario != 'bibliotecario':
        return redirect('index')

    if request.method == 'POST':

        form = BibliotecaForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            biblioteca = form.save(commit=False)

            biblioteca.criado_por = request.user

            biblioteca.save()

            return redirect('painel_bibliotecario')

    else:

        form = BibliotecaForm()

    return render(
        request,
        'bibliotecas/criar.html',
        {
            'form': form
        }
    )