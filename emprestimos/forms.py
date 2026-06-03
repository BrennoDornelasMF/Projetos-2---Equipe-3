from django import forms
from livros.models import Livro

from django import forms
from livros.models import Livro


class DoacaoForm(forms.Form):

    nome_doador = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Nome do doador'
            }
        )
    )

    titulo = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Título do livro'
            }
        )
    )

    autor = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Autor'
            }
        )
    )

    categoria = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Categoria'
            }
        )
    )

    descricao = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-input',
                'placeholder': 'Descrição'
            }
        ),
        required=False
    )

    capa = forms.ImageField(
        required=False
    )

    quantidade = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-input'
            }
        )
    )