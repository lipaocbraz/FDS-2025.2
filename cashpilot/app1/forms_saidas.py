from django import forms
from .models import Saidas

class SaidasForm(forms.ModelForm):
    class Meta:
        model = Saidas
        fields = ['descricao', 'valor', 'data']
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor',
            'data': 'Data',
        }
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }