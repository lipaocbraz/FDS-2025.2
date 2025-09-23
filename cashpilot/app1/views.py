from django.shortcuts import render
from .forms_entradas import EntradasForm
from .forms_saidas import SaidasForm
from .models import Entradas,Saidas

# Create your views here
def index(request):
    return render(request, 'app1/index.html')

def entradas_view(request):
    if request.method != 'POST':
        form = EntradasForm()
    else:
        form = EntradasForm(data=request.POST)
        if form.is_valid():
            form.save()
            form = EntradasForm()
    context = {'form': form}
    return render(request, 'app1/entradas.html', context)

def saidas_view(request):
    if request.method != 'POST':
        form = SaidasForm()
    else:
        form = SaidasForm(data=request.POST)
        if form.is_valid():
            form.save()
            form = SaidasForm()
    context = {'form': form}
    return render(request, 'app1/saidas.html', context)

def extrato_views(request):
    entradas=Entradas.objects.order_by('-date')
    saidas=Saidas.objects.order_by('-date')
    context={'entradas':entradas,'saidas':saidas}
    return render(request,'app1/extrato.html',context)