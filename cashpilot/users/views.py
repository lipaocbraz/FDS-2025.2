from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from .formsLogin import LoginForm
from django.contrib.auth.models import User





# Create your views here.
def cadastro(request):
    errors = []
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password1 = request.POST.get("password1", "").strip()
        password2 = request.POST.get("password2", "").strip()

        # validações básicas
        if not username:
            errors.append("O nome de usuário é obrigatório.")
        if not password1 or not password2:
            errors.append("A senha e a confirmação são obrigatórias.")
        if password1 != password2:
            errors.append("As senhas não coincidem.")
        if User.objects.filter(username=username).exists():
            errors.append("Esse nome de usuário já está em uso.")

        if not errors:
            new_user = User.objects.create_user(
                username=username,
                password=password1
            )
            new_user.save()
            authenticated_user = authenticate(
                username=username,
                password=password1
            )
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('index')

    context = {"errors": errors}
    return render(request, "users/html/cadastro.html", context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def login_view(request):
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['login']
            senha = form.cleaned_data['senha']
            user = authenticate(username=usuario, password=senha)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('nav'))
            else:
                form.add_error(None, "Usuário ou senha inválidos.")
    context = {'form': form}
    return render(request, 'users/html/login.html', context)
