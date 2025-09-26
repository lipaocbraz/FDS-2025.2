from django.shortcuts import render, redirect
from .models import Entradas,Saidas,Saldo
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import matplotlib.pyplot as plt
import numpy as np
# Create your views here
def index(request):
    return render(request, 'app1/html/index.html')
@login_required
def entradas_view(request):
    errors = None
    if request.method == 'POST':
        descricao = request.POST.get("descricao")
        valor = request.POST.get("valor")
        date = request.POST.get("date")

        if descricao and valor and date:
            try:
                entrada = Entradas(
                    descricao=descricao,
                    valor=valor,
                    date=date,
                    owner=request.user
                )
                entrada.save()
                return redirect('entradas')  # volta pra mesma página
            except Exception as e:
                errors = f"Erro ao salvar: {e}"
        else:
            errors = "Todos os campos são obrigatórios."

    context = {"errors": errors}
    return render(request, "app1/html/entradas.html", context)
@login_required
def saidas_view(request):
    errors = []
    selected_descricao = ''
    valor = ''
    date = ''

    if request.method == "POST":
        selected_descricao = request.POST.get("descricao", "").strip()
        valor = request.POST.get("valor", "").strip()
        date = request.POST.get("date", "").strip()

        # validações
        if not selected_descricao:
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

        # salvar se não houver erros
        if not errors:
            Saidas.objects.create(
                descricao=selected_descricao,
                valor=valor,
                date=date,
                owner=request.user
            )
            return redirect("index")

    context = {
        "errors": errors,
        "opcoes_descricao": Saidas.OPCOES_DESCRICAO,
        "selected_descricao": selected_descricao,
        "valor": valor,
        "date": date
    }
    return render(request, "app1/html/saidas.html", context)

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
    total_entradas = Entradas.objects.filter(owner=request.user).aggregate(Sum("valor"))["valor__sum"] or 0
    total_saidas = Saidas.objects.filter(owner=request.user).aggregate(Sum("valor"))["valor__sum"] or 0
    saldo_geral = total_entradas - total_saidas
    saldo = Saldo(owner=request.user, valor=saldo_geral)
    context={'saldo': saldo}
    return render(request,'app1/html/nav.html',context)



def grafico_entradas_saidas(request):
    ano= object.date.year
    mes= object.date.month
    entradas=Entradas.objects.filter(owner=request.user,date__year=ano,date__month=mes).aggregate(Sum("valor"))["valor__sum"] or 0
    saidas=Saidas.objects.filter(owner=request.user,date__year=ano,date__month=mes).aggregate(Sum("valor"))["valor__sum"] or 0
    x = ['Entradas', 'Saídas']
    y = [entradas, saidas]
    posicao=np.arange(len(x))
    largura=0.5
    plt.bar(posicao, y, width=largura, color=['green', 'red'])
    plt.xticks(posicao, x)
    plt.ylabel('Valor')
    plt.title(f'Entradas e Saídas - {mes}/{ano}')

    

    
    