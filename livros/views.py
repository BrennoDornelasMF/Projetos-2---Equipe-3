from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Livro
from .forms import LivroForm
from bibliotecas.models import Biblioteca


@login_required
def buscar_livros(request):

    busca = request.GET.get('busca', '')
    genero = request.GET.get('genero', '')

    livros = Livro.objects.select_related('biblioteca').all()

    if busca:
        livros = livros.filter(
            Q(titulo__icontains=busca) |
            Q(autor__icontains=busca) |
            Q(categoria__icontains=busca)
        )

    if genero:
        livros = livros.filter(genero=genero)

    return render(
        request,
        'livros/buscar.html',
        {
            'livros': livros,
            'busca': busca,
            'genero_selecionado': genero,
            'generos': Livro.GENEROS,
        }
    )


@login_required
def adicionar_livro(request, biblioteca_id):

    biblioteca = get_object_or_404(Biblioteca, id=biblioteca_id)

    if biblioteca.criado_por != request.user and request.user.tipo_usuario != 'admin':
        return redirect('index')

    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES)
        if form.is_valid():
            livro = form.save(commit=False)
            livro.biblioteca = biblioteca
            livro.save()
            return redirect('detalhes_biblioteca', id=biblioteca.id)
    else:
        form = LivroForm()

    return render(
        request,
        'livros/adicionar.html',
        {'form': form, 'biblioteca': biblioteca}
    )


@login_required
def editar_livro(request, livro_id):

    livro = get_object_or_404(Livro, id=livro_id)

    if livro.biblioteca.criado_por != request.user and request.user.tipo_usuario != 'admin':
        return redirect('index')

    if request.method == 'POST':
        form = LivroForm(request.POST, request.FILES, instance=livro)
        if form.is_valid():
            form.save()
            return redirect('detalhes_biblioteca', id=livro.biblioteca.id)
    else:
        form = LivroForm(instance=livro)

    return render(
        request,
        'livros/editar.html',
        {'form': form, 'livro': livro}
    )


@login_required
def excluir_livro(request, livro_id):

    livro = get_object_or_404(Livro, id=livro_id)

    if livro.biblioteca.criado_por != request.user and request.user.tipo_usuario != 'admin':
        return redirect('index')

    biblioteca_id = livro.biblioteca.id
    livro.delete()

    return redirect('detalhes_biblioteca', id=biblioteca_id)