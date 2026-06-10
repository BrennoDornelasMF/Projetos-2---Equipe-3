from django.db import models

from bibliotecas.models import Biblioteca


class Livro(models.Model):

    STATUS = (
        ('disponivel', 'Disponível'),
        ('reservado', 'Reservado'),
        ('indisponivel', 'Indisponível'),
    )

    GENEROS = (
        ('romance', 'Romance'),
        ('ficcao_cientifica', 'Ficção Científica'),
        ('historia', 'História'),
        ('autoajuda', 'Autoajuda'),
        ('biografia', 'Biografia'),
        ('terror', 'Terror'),
        ('fantasia', 'Fantasia'),
        ('outro', 'Outro'),
    )
    
    titulo = models.CharField(max_length=200)

    autor = models.CharField(max_length=200)

    categoria = models.CharField(max_length=100)

    genero = models.CharField(
        max_length=50,
        choices=GENEROS,
        default='outro'
    )

    descricao = models.TextField()

    capa = models.ImageField(
        upload_to='livros/',
        blank=True,
        null=True
    )

    quantidade = models.IntegerField(default=1)

    disponivel = models.BooleanField(default=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='disponivel'
    )

    biblioteca = models.ForeignKey(
        Biblioteca,
        on_delete=models.CASCADE,
        related_name='livros'
    )

    def __str__(self):
        return self.titulo