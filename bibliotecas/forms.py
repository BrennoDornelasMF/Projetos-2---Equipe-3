from django import forms

from .models import Biblioteca


class BibliotecaForm(forms.ModelForm):

    class Meta:

        model = Biblioteca

        fields = [
            'nome',
            'endereco',
            'cidade',
            'estado',
            'descricao',
            'imagem'
        ]