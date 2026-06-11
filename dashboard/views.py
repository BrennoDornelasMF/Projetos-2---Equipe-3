from django.shortcuts import (
    render,
    redirect
)

from django.contrib.auth.decorators import login_required
from django.utils import timezone

from bibliotecas.models import Biblioteca
from livros.models import Livro
from emprestimos.models import Emprestimo, Sugestao


@login_required
def dashboard(request):

    user = request.user  # ← mover para cá

    if user.tipo_usuario == 'admin':

        filtro_status = request.GET.get('status', '')
        filtro_biblioteca = request.GET.get('biblioteca', '')
        ordenar = request.GET.get('ordenar', 'votos')

        sugestoes = Sugestao.objects.select_related('biblioteca', 'leitor')

        if filtro_status:
            sugestoes = sugestoes.filter(status=filtro_status)

        if filtro_biblioteca:
            sugestoes = sugestoes.filter(biblioteca_id=filtro_biblioteca)

        if ordenar == 'votos':
            sugestoes = sugestoes.order_by('-votos', '-criado_em')
        elif ordenar == 'recentes':
            sugestoes = sugestoes.order_by('-criado_em')
        elif ordenar == 'antigas':
            sugestoes = sugestoes.order_by('criado_em')

        total_sugestoes = Sugestao.objects.count()
        total_pendentes = Sugestao.objects.filter(status='pendente').count()
        total_aprovadas = Sugestao.objects.filter(status='aprovada').count()
        total_recusadas = Sugestao.objects.filter(status='recusada').count()

        context = {
            'tipo': 'admin',
            'total_bibliotecas': Biblioteca.objects.count(),
            'total_livros': Livro.objects.count(),
            'emprestimos_ativos': Emprestimo.objects.filter(status='emprestado').count(),
            'emprestimos_pendentes': Emprestimo.objects.filter(status='pendente').count(),
            'bibliotecas': Biblioteca.objects.all(),
            'sugestoes': sugestoes,
            'total_sugestoes': total_sugestoes,
            'total_pendentes': total_pendentes,
            'total_aprovadas': total_aprovadas,
            'total_recusadas': total_recusadas,
            'filtro_status': filtro_status,
            'filtro_biblioteca': filtro_biblioteca,
            'ordenar': ordenar,
        }
        return render(request, 'dashboard/admin.html', context)


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

        emprestimos_ativos_qs = Emprestimo.objects.filter(
            biblioteca__criado_por=user,
            status='emprestado'
        ).select_related('livro', 'leitor', 'biblioteca').order_by('data_devolucao')

        emprestimos_pendentes_qs = Emprestimo.objects.filter(
            biblioteca__criado_por=user,
            status='pendente'
        ).select_related('livro', 'leitor', 'biblioteca').order_by('data_emprestimo')

        emprestimos_com_prazo = []
        for e in emprestimos_ativos_qs:
            dias = e.dias_restantes()
            if dias is not None and dias < 0:
                situacao = 'atrasado'
            elif dias is not None and dias <= 3:
                situacao = 'urgente'
            else:
                situacao = 'ok'
            emprestimos_com_prazo.append({
                'emprestimo': e,
                'dias_restantes': dias,
                'situacao': situacao,
            })

        context = {

            'tipo': 'bibliotecario',

            'total_bibliotecas':
                bibliotecas.count(),

            'total_livros':
                livros.count(),

            'emprestimos_ativos':
                emprestimos_ativos_qs.count(),

            'emprestimos_pendentes':
                emprestimos_pendentes_qs.count(),

            'bibliotecas':
                bibliotecas,

            'emprestimos_com_prazo':
                emprestimos_com_prazo,

            'emprestimos_pendentes_lista':
                emprestimos_pendentes_qs,
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