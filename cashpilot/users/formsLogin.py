from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    login = forms.CharField(label='Usuário', max_length=50)
    senha = forms.CharField(label='Senha', max_length=50, widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('login')
        password = cleaned_data.get('senha')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise ValidationError("Usuário ou senha inválidos.")
            cleaned_data['user'] = user  # guarda o usuário autenticado
        return cleaned_data
