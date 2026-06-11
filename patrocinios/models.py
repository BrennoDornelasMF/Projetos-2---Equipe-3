from django.db import models
from bibliotecas.models import Biblioteca


class Patrocinio(models.Model):

    nome_patrocinador = models.CharField(max_length=200)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    descricao = models.TextField(blank=True)

    data = models.DateField(auto_now_add=True)

    biblioteca = models.ForeignKey(
        Biblioteca,
        on_delete=models.CASCADE,
        related_name='patrocinios'
    )

    def __str__(self):
        return f'{self.nome_patrocinador} - {self.biblioteca}'