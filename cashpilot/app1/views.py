from django.shortcuts import render, redirect
from .models import Entradas,Saidas
from django.contrib.auth.decorators import login_required
# Create your views here
def index(request):
    return render(request, 'app1/html/index.html')
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
    errors = []
    if request.method == "POST":
        descricao = request.POST.get("descricao", "").strip()
        valor = request.POST.get("valor", "").strip()
        date = request.POST.get("date", "").strip()

        # Validações simples
        if not descricao:
            errors.append("A descrição é obrigatória.")
        if not valor:
            errors.append("O valor é obrigatório.")
        else:
            try:
                valor = float(valor)
            except ValueError:
                errors.append("O valor deve ser numérico.")

        if not date:
            errors.append("A data é obrigatória.")

        # Se não houver erros, salvar
        if not errors:
            saida = Saidas.objects.create(
                descricao=descricao,
                valor=valor,
                date=date,
                owner=request.user
            )
            return redirect("index")  # depois de salvar, redireciona

    context = {"errors": errors}
    return render(request, "app1/html/saidas.html", context)
@login_required
def extrato_views(request):
    entradas=Entradas.objects.filter(owner=request.user).order_by('-date')
    saidas=Saidas.objects.filter(owner=request.user).order_by('-date')
    context={'entradas':entradas,'saidas':saidas}
    return render(request,'app1/html/extrato.html',context)
@login_required
def nav_view(request):
    return render(request,'app1/html/nav.html')