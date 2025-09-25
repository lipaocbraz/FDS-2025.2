from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from .formsLogin import LoginForm
from django.contrib.auth.models import User

def login_view(request):
    errors = None
    
    if request.method != 'POST':
        usuario = ""
        senha = ""
    else:
        usuario = request.POST.get("login")
        senha = request.POST.get("senha")

        if usuario and senha:
            user = authenticate(username=usuario, password=senha)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('nav'))
            else:
                errors = "Usuário ou senha inválidos."
        else:
            errors = "Preencha todos os campos."

    context = {
        'usuario': usuario,
        'senha': senha,
        'errors': errors,
    }
    return render(request, 'users/html/login.html', context)
