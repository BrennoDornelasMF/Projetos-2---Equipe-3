import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ.get('SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('SUPERUSER_EMAIL', 'admin@admin.com')
        password = os.environ.get('SUPERUSER_PASSWORD')

        if not password:
            self.stdout.write('SUPERUSER_PASSWORD não definida, pulando.')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Usuário {username} já existe, pulando.')
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        self.stdout.write(f'Superuser {username} criado com sucesso!')