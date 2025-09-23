from django import forms
from .models import Entradas

class EntradasForm(forms.ModelForm):
    class Meta:
        model = Entradas
        fields = ['descricao', 'valor', 'date']
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor',
            'date': 'Date',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
