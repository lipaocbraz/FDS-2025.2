from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Nome de usuário",
        help_text="",  
    )
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        help_text="Sua senha deve ter pelo menos 8 caracteres e não pode ser muito comum.",
    )
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput,
        help_text="Digite a mesma senha novamente para confirmação.",
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")
