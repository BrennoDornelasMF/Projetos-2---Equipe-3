from django.db import models

from django.conf import settings

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