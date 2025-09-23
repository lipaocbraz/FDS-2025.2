from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from .forms import CustomUserCreationForm
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
