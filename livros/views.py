from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import (
    Emprestimo,
    Doacao,
    AvisoDisponibilidade,
    Sugestao,
    VotoSugestao,
    Desafio,
    ParticipacaoDesafio,
)
from .forms import DoacaoForm, SugestaoForm, DesafioForm

from livros.models import Livro
from bibliotecas.models import Biblioteca


# ─────────────────────────────────────────
# EMPRÉSTIMOS
# ─────────────────────────────────────────

@login_required
def solicitar_emprestimo(request, livro_id):

    livro = get_object_or_404(Livro, id=livro_id)

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

    biblioteca = get_object_or_404(Biblioteca, id=biblioteca_id)

    if biblioteca.criado_por != request.user and request.user.tipo_usuario != 'admin':
        return redirect('index')

    emprestimos = Emprestimo.objects.filter(
        biblioteca=biblioteca
    ).select_related('livro', 'leitor').order_by('-data_emprestimo')

    atrasados = [e for e in emprestimos if e.esta_atrasado()]

    return render(
        request,
        'emprestimos/painel.html',
        {
            'biblioteca': biblioteca,
            'emprestimos': emprestimos,
            'total_atrasados': len(atrasados),
        }
    )


@login_required
def aceitar_emprestimo(request, id):

    emprestimo = get_object_or_404(Emprestimo, id=id)

    if request.user != emprestimo.biblioteca.criado_por and request.user.tipo_usuario != 'admin':
        return redirect('index')

    if request.method == 'POST':

        dias = int(request.POST.get('dias'))

        emprestimo.status = 'emprestado'
        emprestimo.data_devolucao = timezone.now().date() + timedelta(days=dias)
        emprestimo.save()

        livro = emprestimo.livro
        livro.quantidade -= 1
        if livro.quantidade <= 0:
            livro.disponivel = False
        livro.save()

        return redirect('painel_emprestimos', emprestimo.biblioteca.id)

    return render(
        request,
        'emprestimos/aceitar.html',
        {'emprestimo': emprestimo}
    )


@login_required
def devolver_livro(request, emprestimo_id):

    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)

    if emprestimo.biblioteca.criado_por != request.user and request.user.tipo_usuario != 'admin':
        return redirect('index')

    emprestimo.status = 'devolvido'
    emprestimo.save()

    livro = emprestimo.livro
    livro.quantidade += 1
    livro.disponivel = True
    livro.save()

    # notificar leitores que estão aguardando este livro
    avisos = AvisoDisponibilidade.objects.filter(
        livro=livro,
        ativo=True,
        notificado=False
    )
    avisos.update(notificado=True)

    return redirect(
        'painel_emprestimos',
        biblioteca_id=emprestimo.biblioteca.id
    )


@login_required
def devolver_emprestimo(request, id):
    return devolver_livro(request, emprestimo_id=id)


@login_required
def leitores_ativos(request, biblioteca_id):

    biblioteca = get_object_or_404(Biblioteca, id=biblioteca_id)

    if biblioteca.criado_por != request.user and request.user.tipo_usuario != 'admin':
        return redirect('index')

    emprestimos = Emprestimo.objects.filter(
        biblioteca=biblioteca,
        status='emprestado'
    ).select_related('leitor', 'livro').order_by('data_devolucao')

    return render(
        request,
        'emprestimos/leitores_ativos.html',
        {
            'biblioteca': biblioteca,
            'emprestimos': emprestimos,
        }
    )


# ─────────────────────────────────────────
# DOAÇÃO
# ─────────────────────────────────────────

@login_required
def registrar_doacao(request, biblioteca_id):

    biblioteca = get_object_or_404(Biblioteca, id=biblioteca_id)

    if biblioteca.criado_por != request.user and request.user.tipo_usuario != 'admin':
        return redirect('index')

    if request.method == 'POST':

        form = DoacaoForm(request.POST, request.FILES)

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

            return redirect('detalhes_biblioteca', id=biblioteca.id)

    else:
        form = DoacaoForm()

    return render(
        request,
        'emprestimos/doacao.html',
        {'form': form, 'biblioteca': biblioteca}
    )


# ─────────────────────────────────────────
# AVISOS DE DISPONIBILIDADE
# ─────────────────────────────────────────

@login_required
def ativar_aviso(request, livro_id):

    livro = get_object_or_404(Livro, id=livro_id)

    if request.user.tipo_usuario != 'leitor':
        return redirect('index')

    AvisoDisponibilidade.objects.get_or_create(
        livro=livro,
        leitor=request.user,
        defaults={'ativo': True}
    )

    return redirect('detalhes_biblioteca', id=livro.biblioteca.id)


@login_required
def meus_avisos(request):

    if request.user.tipo_usuario != 'leitor':
        return redirect('index')

    avisos = AvisoDisponibilidade.objects.filter(
        leitor=request.user
    ).select_related('livro', 'livro__biblioteca').order_by('-criado_em')

    return render(
        request,
        'emprestimos/avisos.html',
        {'avisos': avisos}
    )


# ─────────────────────────────────────────
# SUGESTÕES
# ─────────────────────────────────────────

@login_required
def listar_sugestoes(request):

    sugestoes = Sugestao.objects.select_related(
        'biblioteca', 'leitor'
    ).order_by('-votos', '-criado_em')

    ja_votei = set(
        VotoSugestao.objects.filter(
            leitor=request.user
        ).values_list('sugestao_id', flat=True)
    )

    return render(
        request,
        'emprestimos/sugestoes.html',
        {
            'sugestoes': sugestoes,
            'ja_votei': ja_votei,
        }
    )


@login_required
def sugerir_titulo(request):

    if request.user.tipo_usuario != 'leitor':
        return redirect('index')

    if request.method == 'POST':

        form = SugestaoForm(request.POST)

        if form.is_valid():
            sugestao = form.save(commit=False)
            sugestao.leitor = request.user
            sugestao.save()
            return redirect('listar_sugestoes')

    else:
        form = SugestaoForm()

    return render(
        request,
        'emprestimos/sugerir.html',
        {'form': form}
    )


@login_required
def votar_sugestao(request, sugestao_id):

    sugestao = get_object_or_404(Sugestao, id=sugestao_id)

    _, criado = VotoSugestao.objects.get_or_create(
        sugestao=sugestao,
        leitor=request.user
    )

    if criado:
        sugestao.votos += 1
        sugestao.save()

    return redirect('listar_sugestoes')


@login_required
def gerenciar_sugestao(request, sugestao_id):

    if request.user.tipo_usuario not in ('bibliotecario', 'admin'):
        return redirect('index')

    sugestao = get_object_or_404(Sugestao, id=sugestao_id)

    if request.user.tipo_usuario == 'bibliotecario':
        if sugestao.biblioteca.criado_por != request.user:
            return redirect('index')

    acao = request.POST.get('acao')

    if acao == 'aprovar':
        sugestao.status = 'aprovada'
    elif acao == 'recusar':
        sugestao.status = 'recusada'

    sugestao.save()

    return redirect('listar_sugestoes')


# ─────────────────────────────────────────
# DESAFIOS
# ─────────────────────────────────────────

@login_required
def listar_desafios(request):

    desafios = Desafio.objects.select_related('biblioteca').order_by('-criado_em')

    participacoes = {}

    if request.user.tipo_usuario == 'leitor':
        for p in ParticipacaoDesafio.objects.filter(leitor=request.user):
            participacoes[p.desafio_id] = p

    return render(
        request,
        'emprestimos/desafios.html',
        {
            'desafios': desafios,
            'participacoes': participacoes,
        }
    )


@login_required
def participar_desafio(request, desafio_id):

    if request.user.tipo_usuario != 'leitor':
        return redirect('index')

    desafio = get_object_or_404(Desafio, id=desafio_id)

    ParticipacaoDesafio.objects.get_or_create(
        desafio=desafio,
        leitor=request.user
    )

    return redirect('listar_desafios')


@login_required
def criar_desafio(request, biblioteca_id):

    biblioteca = get_object_or_404(Biblioteca, id=biblioteca_id)

    if biblioteca.criado_por != request.user and request.user.tipo_usuario != 'admin':
        return redirect('index')

    if request.method == 'POST':

        form = DesafioForm(request.POST)

        if form.is_valid():
            desafio = form.save(commit=False)
            desafio.biblioteca = biblioteca
            desafio.save()
            return redirect('listar_desafios')

    else:
        form = DesafioForm()

    return render(
        request,
        'emprestimos/criar_desafio.html',
        {'form': form, 'biblioteca': biblioteca}
    )