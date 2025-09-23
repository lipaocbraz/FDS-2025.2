from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from .forms import CustomUserCreationForm
from .formsLogin import LoginForm



# Create your views here.

def cadastro(request):
    if request.method != 'POST':
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            authenticated_user = authenticate(
                username=new_user.username,
                password=request.POST['password1']
            )
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('index'))
    context = {'form': form}
    return render(request, 'users/html/cadastro.html', context)

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
