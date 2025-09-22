from django import forms
from .models import Saidas

class SaidasForm(forms.ModelForm):
    class Meta:
        model = Saidas
        fields = ['descricao', 'valor', 'date']
        labels = {
            'descricao': 'Descrição',
            'valor': 'Valor',
            'date': 'Date',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }