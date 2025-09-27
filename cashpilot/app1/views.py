from django.shortcuts import render, redirect
from .models import Entradas,Saidas,Saldo
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import matplotlib.pyplot as plt
import numpy as np
import datetime
from django.utils import timezone
from datetime import date 


def index(request):
    return render(request, 'app1/html/index.html')

@login_required
def entradas_view(request):
    errors = None
    if request.method == 'POST':
        descricao = request.POST.get("descricao")
        valor = request.POST.get("valor")
        date_str = request.POST.get("date") 

        if descricao and valor and date_str:
            try:
                valor = float(valor)
                entrada = Entradas(
                    descricao=descricao,
                    valor=valor,
                    date=date_str, 
                    owner=request.user
                )
                entrada.save()
                Saldo.criar_registro_saldo_apos_transacao(request.user)
                
                return redirect('entradas')  
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
    date_str = ''

    if request.method == "POST":
        selected_descricao = request.POST.get("descricao", "").strip()
        valor = request.POST.get("valor", "").strip()
        date_str = request.POST.get("date", "").strip()

        
        if not selected_descricao:
            errors.append("A descrição é obrigatória.")
        if not valor:
            errors.append("O valor é obrigatório.")
        else:
            try:
                valor = float(valor)
            except ValueError:
                errors.append("O valor deve ser numérico.")
        if not date_str:
            errors.append("A data é obrigatória.")

        
        if not errors:
            Saidas.objects.create(
                descricao=selected_descricao,
                valor=valor,
                date=date_str,
                owner=request.user
            )
            
            
            Saldo.criar_registro_saldo_apos_transacao(request.user)
            
            return redirect("saidas")

    context = {
        "errors": errors,
        "opcoes_descricao": Saidas.OPCOES_DESCRICAO,
        "selected_descricao": selected_descricao,
        "valor": valor,
        "date": date_str
    }
    return render(request, "app1/html/saidas.html", context)

@login_required
def extrato_views(request):
    entradas=Entradas.objects.filter(owner=request.user).order_by('-date')
    saidas=Saidas.objects.filter(owner=request.user).order_by('-date')
    context={'entradas':entradas,'saidas':saidas}
    return render(request,'app1/html/extrato.html',context)

@login_required
def nav_view(request):
    
    try:
        
        saldo = Saldo.objects.filter(owner=request.user).latest('data_registro')
    except Saldo.DoesNotExist:
        
        saldo = Saldo(owner=request.user, valor=0.0)
        
    context={'saldo': saldo}
    return render(request,'app1/html/nav.html',context)

@login_required
def grafico_entradas_saidas(request):
    
    hoje = datetime.date.today()
    ano = hoje.year
    mes = hoje.month
    
    
    entradas = Entradas.objects.filter(owner=request.user, date__year=ano, date__month=mes).aggregate(Sum("valor"))["valor__sum"] or 0
    saidas = Saidas.objects.filter(owner=request.user, date__year=ano, date__month=mes).aggregate(Sum("valor"))["valor__sum"] or 0
    
    x = ['Entradas', 'Saídas']
    y = [entradas, saidas]
    posicao=np.arange(len(x))
    largura=0.5
    plt.bar(posicao, y, width=largura, color=['green', 'red'])
    plt.xticks(posicao, x)
    plt.ylabel('Valor')
    plt.title(f'Entradas e Saídas - {mes}/{ano}')



@login_required
def grafico_saldo(request):
    ano = datetime.date.today().year 
    
    saldos_anuais = []
    
    
    for mes in range(1, 13):
        try:
            ultimo_saldo = Saldo.objects.filter(
                owner=request.user,
                data_registro__year=ano,
                data_registro__month=mes
            ).latest('data_registro')
            saldos_anuais.append(ultimo_saldo.valor)
        except Saldo.DoesNotExist:
            saldos_anuais.append(0) 

    
    meses_rotulos = range(1, 13)
    saldo_positivo = [s if s > 0 else 0 for s in saldos_anuais]
    saldo_negativo = [abs(s) if s < 0 else 0 for s in saldos_anuais] 

    x = np.arange(len(meses_rotulos))
    largura = 0.35
    plt.figure(figsize=(10,5))
    
    plt.bar(x - largura/2, saldo_positivo, width=largura, color='green', label='Positivo')
    plt.bar(x + largura/2, saldo_negativo, width=largura, color='red', label='Negativo')
    plt.xticks(x, [f'Mês {m}' for m in meses_rotulos])
    plt.ylabel('Valor')
    plt.title(f'Análise do Saldo Mensal (Final do Mês) - Ano {ano}')
    plt.legend()