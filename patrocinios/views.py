from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from .models import Patrocinio
from .forms import PatrocinioForm
from bibliotecas.models import Biblioteca


@login_required
def registrar_patrocinio(request, biblioteca_id):

    biblioteca = get_object_or_404(
        Biblioteca,
        id=biblioteca_id
    )

    if biblioteca.criado_por != request.user:
        return redirect('index')

    if request.method == 'POST':

        form = PatrocinioForm(request.POST)

        if form.is_valid():

            patrocinio = form.save(commit=False)
            patrocinio.biblioteca = biblioteca
            patrocinio.save()

            return redirect(
                'detalhes_biblioteca',
                id=biblioteca.id
            )

    else:

        form = PatrocinioForm()

    return render(
        request,
        'patrocinios/registrar.html',
        {
            'form': form,
            'biblioteca': biblioteca
        }
    )


@login_required
def listar_patrocinios(request, biblioteca_id):

    biblioteca = get_object_or_404(
        Biblioteca,
        id=biblioteca_id
    )

    if biblioteca.criado_por != request.user:
        return redirect('index')

    patrocinios = Patrocinio.objects.filter(
        biblioteca=biblioteca
    ).order_by('-data')

    return render(
        request,
        'patrocinios/lista.html',
        {
            'biblioteca': biblioteca,
            'patrocinios': patrocinios
        }
    )