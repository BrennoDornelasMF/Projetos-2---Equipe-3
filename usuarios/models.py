from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Usuario(AbstractUser):

    TIPOS = (
        ('leitor', 'Leitor'),
        ('bibliotecario', 'Bibliotecário'),
    )

    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPOS,
        default='leitor'
    )