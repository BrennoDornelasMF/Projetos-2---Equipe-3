from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):

    TIPOS = (
        ('leitor', 'Leitor'),
        ('bibliotecario', 'Bibliotecário'),
        ('admin', 'Administrador'),
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPOS,
        default='leitor'
    )

    nome_completo = models.CharField(
        max_length=300,
        blank=True
    )

    cpf = models.CharField(
        max_length=14,
        blank=True
    )

    telefone = models.CharField(
        max_length=20,
        blank=True
    )

    data_nascimento = models.DateField(
        null=True,
        blank=True
    )

    cep = models.CharField(
        max_length=10,
        blank=True
    )

    rua = models.CharField(
        max_length=300,
        blank=True
    )

    numero = models.CharField(
        max_length=10,
        blank=True
    )

    bairro = models.CharField(
        max_length=200,
        blank=True
    )

    cidade = models.CharField(
        max_length=200,
        blank=True
    )

    estado = models.CharField(
        max_length=100,
        blank=True
    )