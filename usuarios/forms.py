from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class CadastroForm(UserCreationForm):

    class Meta:

        model = Usuario

        fields = [
            'username',
            'email',
            'tipo_usuario',
            'nome_completo',
            'cpf',
            'telefone',
            'data_nascimento',
            'cep',
            'rua',
            'numero',
            'bairro',
            'cidade',
            'estado',
            'password1',
            'password2'
        ]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'}),
            'tipo_usuario': forms.Select(attrs={'class': 'form-input'}),
            'nome_completo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '000.000.000-00'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '(00) 00000-0000'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'cep': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '00000-000'}),
            'rua': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Rua'}),
            'numero': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Número'}),
            'bairro': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Estado'}),
        }

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Senha'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirmar senha'})
    )