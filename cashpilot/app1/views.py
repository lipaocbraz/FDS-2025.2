from django.shortcuts import render
from .forms_entradas import EntradasForm
from .forms_saidas import SaidasForm

# Create your views here.
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
