from django import forms
from .models import Entradas

class EntradasForm(forms.ModelForm):
    class meta:
        model = Entradas
        fields = ['descricao', 'valor', 'data']
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor',
            'data': 'Data',
        }
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
