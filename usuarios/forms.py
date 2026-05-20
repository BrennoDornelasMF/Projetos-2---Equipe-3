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
            'password1',
            'password2'
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Usuário'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Email'
                }
            ),

            'tipo_usuario': forms.Select(
                attrs={
                    'class': 'form-input'
                }
            ),
        }

    password1 = forms.CharField(

        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Senha'
            }
        )
    )

    password2 = forms.CharField(

        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Confirmar senha'
            }
        )
    )