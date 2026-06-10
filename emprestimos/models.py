from django.db import models
from django.conf import settings
from django.utils import timezone

from livros.models import Livro
from bibliotecas.models import Biblioteca


class Emprestimo(models.Model):

    STATUS = (
        ('pendente', 'Pendente'),
        ('emprestado', 'Emprestado'),
        ('devolvido', 'Devolvido'),
    )

    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE
    )

    leitor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    biblioteca = models.ForeignKey(
        Biblioteca,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pendente'
    )

    data_emprestimo = models.DateTimeField(
        auto_now_add=True
    )

    data_devolucao = models.DateField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f'{self.leitor} - {self.livro}'

    def dias_restantes(self):
        if self.data_devolucao and self.status == 'emprestado':
            return (self.data_devolucao - timezone.now().date()).days
        return None

    def esta_atrasado(self):
        dias = self.dias_restantes()
        if dias is not None:
            return dias < 0
        return False


class Doacao(models.Model):

    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        related_name='doacoes'
    )

    biblioteca = models.ForeignKey(
        Biblioteca,
        on_delete=models.CASCADE,
        related_name='doacoes'
    )

    nome_doador = models.CharField(max_length=200)

    quantidade = models.IntegerField(default=1)

    data_doacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome_doador} - {self.livro}'


class AvisoDisponibilidade(models.Model):

    livro = models.ForeignKey(
        Livro,
        on_delete=models.CASCADE,
        related_name='avisos'
    )

    leitor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avisos'
    )

    ativo = models.BooleanField(default=True)

    notificado = models.BooleanField(default=False)

    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('livro', 'leitor')

    def __str__(self):
        return f'{self.leitor} aguarda {self.livro}'


class Sugestao(models.Model):

    STATUS = (
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('recusada', 'Recusada'),
    )

    titulo = models.CharField(max_length=200)

    autor = models.CharField(max_length=200)

    descricao = models.TextField(blank=True)

    biblioteca = models.ForeignKey(
        Biblioteca,
        on_delete=models.CASCADE,
        related_name='sugestoes'
    )

    leitor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sugestoes'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='pendente'
    )

    votos = models.IntegerField(default=0)

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} - {self.biblioteca}'


class VotoSugestao(models.Model):

    sugestao = models.ForeignKey(
        Sugestao,
        on_delete=models.CASCADE,
        related_name='votantes'
    )

    leitor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('sugestao', 'leitor')


class Desafio(models.Model):

    titulo = models.CharField(max_length=200)

    descricao = models.TextField()

    biblioteca = models.ForeignKey(
        Biblioteca,
        on_delete=models.CASCADE,
        related_name='desafios'
    )

    meta = models.IntegerField(
        default=1,
        help_text='Quantidade de livros a ler'
    )

    data_fim = models.DateField()

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    def esta_ativo(self):
        return self.data_fim >= timezone.now().date()


class ParticipacaoDesafio(models.Model):

    desafio = models.ForeignKey(
        Desafio,
        on_delete=models.CASCADE,
        related_name='participacoes'
    )

    leitor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='desafios_participando'
    )

    livros_lidos = models.IntegerField(default=0)

    concluido = models.BooleanField(default=False)

    data_participacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('desafio', 'leitor')

    def __str__(self):
        return f'{self.leitor} - {self.desafio}'

    def progresso_percentual(self):
        if self.desafio.meta > 0:
            return min(
                int((self.livros_lidos / self.desafio.meta) * 100),
                100
            )
        return 0