from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
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

def cadastro(request):
    errors = []
    username = ""
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        if not username:
            errors.append("O nome de usuário é obrigatório.")
        if not password1 or not password2:
            errors.append("A senha e a confirmação são obrigatórias.")
        elif password1 != password2:
            errors.append("As senhas não coincidem.")
        elif User.objects.filter(username=username).exists():
            errors.append("Esse nome de usuário já está em uso.")

        if not errors:
            user = User.objects.create_user(username=username, password=password1)
            authenticated_user = authenticate(username=username, password=password1)
            
            if authenticated_user:
                login(request, authenticated_user)
                return redirect("index")

    context = {"errors": errors, "username": username}
    return render(request, "users/html/cadastro.html", context)

def logout_view(request):
    logout(request)
    return redirect('login')