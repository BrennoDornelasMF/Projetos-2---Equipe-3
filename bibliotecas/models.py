from django.db import models
from usuarios.models import Usuario


class Biblioteca(models.Model):

    nome = models.CharField(max_length=200)

    endereco = models.CharField(max_length=300)

    cidade = models.CharField(max_length=100)

    estado = models.CharField(max_length=100)

    descricao = models.TextField()

    imagem = models.ImageField(
        upload_to='bibliotecas/',
        blank=True,
        null=True
    )

    criado_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='bibliotecas'
    )

    def __str__(self):
        return self.nome