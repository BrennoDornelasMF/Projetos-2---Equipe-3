from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from .models import Livro
from .forms import LivroForm

from bibliotecas.models import Biblioteca


@login_required
def adicionar_livro(request, biblioteca_id):

    biblioteca = get_object_or_404(
        Biblioteca,
        id=biblioteca_id
    )

    if biblioteca.criado_por != request.user:
        return redirect('index')

    if request.method == 'POST':

        form = LivroForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            livro = form.save(commit=False)

            livro.biblioteca = biblioteca

            livro.save()

            return redirect(
                'detalhes_biblioteca',
                id=biblioteca.id
            )

    else:

        form = LivroForm()

    return render(
        request,
        'livros/adicionar.html',
        {
            'form': form,
            'biblioteca': biblioteca
        }
    )