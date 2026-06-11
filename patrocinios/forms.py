from django import forms
from .models import Patrocinio


class PatrocinioForm(forms.ModelForm):

    class Meta:

        model = Patrocinio

        fields = [
            'nome_patrocinador',
            'valor',
            'descricao'
        ]