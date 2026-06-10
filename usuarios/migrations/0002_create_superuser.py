from django.db import migrations
import os

def create_superuser(apps, schema_editor):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    username = os.environ.get('SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('SUPERUSER_EMAIL', 'admin@admin.com')
    password = os.environ.get('SUPERUSER_PASSWORD')

    print(f">>> SUPERUSER_USERNAME: {username}")
    print(f">>> SUPERUSER_EMAIL: {email}")
    print(f">>> SUPERUSER_PASSWORD existe: {bool(password)}")

    if password:
        User.objects.filter(username=username).delete()
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f">>> Superuser criado: {user.username} | is_staff: {user.is_staff} | is_superuser: {user.is_superuser}")
    else:
        print(">>> ERRO: SUPERUSER_PASSWORD não encontrada nas variáveis de ambiente!")

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]