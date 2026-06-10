from django import forms

from .models import Doacao, Sugestao, Desafio
from livros.models import Livro
from bibliotecas.models import Biblioteca


class DoacaoForm(forms.Form):

    titulo = forms.CharField(max_length=200)
    autor = forms.CharField(max_length=200)
    categoria = forms.CharField(max_length=100)
    descricao = forms.CharField(widget=forms.Textarea, required=False)
    capa = forms.ImageField(required=False)
    quantidade = forms.IntegerField(min_value=1)
    nome_doador = forms.CharField(max_length=200)


class SugestaoForm(forms.ModelForm):

    class Meta:
        model = Sugestao
        fields = ['titulo', 'autor', 'descricao', 'biblioteca']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Título do livro'}),
            'autor': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome do autor'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'placeholder': 'Por que este livro é importante?', 'rows': 3}),
            'biblioteca': forms.Select(attrs={'class': 'form-input'}),
        }


class DesafioForm(forms.ModelForm):

    class Meta:
        model = Desafio
        fields = ['titulo', 'descricao', 'meta', 'data_fim']

        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'meta': forms.NumberInput(attrs={'class': 'form-input', 'min': 1}),
            'data_fim': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
        }