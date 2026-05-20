from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q

from livros.models import Livro
from .forms import BibliotecaForm
from .models import Biblioteca

@login_required
def bibliotecas_leitor(request):

    if request.user.tipo_usuario != 'leitor':
        return redirect('index')

    busca = request.GET.get('busca')

    bibliotecas = Biblioteca.objects.all()

    if busca:

        bibliotecas = bibliotecas.filter(

            Q(cidade__icontains=busca) |

            Q(estado__icontains=busca) |

            Q(nome__icontains=busca)
        )

    return render(
        request,
        'bibliotecas/lista_bibliotecas.html',
        {
            'bibliotecas': bibliotecas
        }
    )

@login_required
def detalhes_biblioteca(request, id):

    biblioteca = get_object_or_404(
        Biblioteca,
        id=id
    )

    livros = Livro.objects.filter(
        biblioteca=biblioteca
    )

    is_dono = (
        request.user == biblioteca.criado_por
    )

    return render(
        request,
        'bibliotecas/detalhes.html',
        {
            'biblioteca': biblioteca,
            'livros': livros,
            'is_dono': is_dono
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