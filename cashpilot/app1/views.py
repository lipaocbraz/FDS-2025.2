from django.shortcuts import render
from .forms_entradas import EntradasForm
from .forms_saidas import SaidasForm
from .models import Entradas,Saidas
from django.contrib.auth.decorators import login_required
# Create your views here
def index(request):
    return render(request, 'app1/index.html')
@login_required
def entradas_view(request):
    if request.method != 'POST':
        form = EntradasForm()
    else:
        form = EntradasForm(data=request.POST)
        if form.is_valid():
            entrada= form.save(commit=False)
            entrada.owner=request.user
            entrada.save()
            form.save()
            form = EntradasForm()
    context = {'form': form}
    return render(request, 'app1/html/entradas.html', context)
@login_required
def saidas_view(request):
    if request.method != 'POST':
        form = SaidasForm()
    else:
        form = SaidasForm(data=request.POST)
        if form.is_valid():
            saida= form.save(commit=False)
            saida.owner=request.user
            saida.save()
            form.save()
            form = SaidasForm()
    context = {'form': form}
    return render(request, 'app1/html/saidas.html', context)
@login_required
def extrato_views(request):
    entradas=Entradas.objects.filter(ower=request.user).order_by('-date')
    saidas=Saidas.objects.filter(ower=request.user).order_by('-date')
    context={'entradas':entradas,'saidas':saidas}
    return render(request,'app1/html/extrato.html',context)
@login_required
def nav_view(request):
    return render(request,'app1/html/nav.html')