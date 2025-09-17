from datetime import date
from django.db import models
from django.db.models import Sum
from django.utils import timezone

class Entradas(models.Model):
    descricao=models.CharField(max_length=100)
    valor=models.DecimalField(default=0.0,verbose_name="valor ganho R$",max_digits=15,decimal_places=2,null=False,blank=False)
    date=models.DateField(default=timezone.now)
    def __str__(self):
        return self.descricao[:15]+ "... - R$ " + str(self.valor)
class Saidas(models.Model):
    descricao=models.CharField(max_length=100)
    valor=models.DecimalField(default=0.0,verbose_name="valor gasto R$",max_digits=15,decimal_places=2,null=False,blank=False)
    date=models.DateField(default=timezone.now)
    def __str__(self):
        return self.descricao[:15]+ "... - R$ " + str(self.valor)


class Saldo(models.Model):
    valor = models.DecimalField(
        default=0.0,
        verbose_name="Saldo R$",
        max_digits=15,
        decimal_places=2
    )
    mes_inicio=models.DateField(verbose_name="data inicial")
    mes_fim=models.DateField(verbose_name="data final")
    mes_atualizacao = models.DateField(auto_now=True, verbose_name="data de atualização")

    def calcular_saldo(self, data_inicio, data_fim):
        total_entradas = Entradas.objects.filter(date__range=(data_inicio, data_fim)).aggregate(Sum("valor"))["valor__sum"] or 0
        total_saidas = Saidas.objects.filter(date__range=(data_inicio, data_fim)).aggregate(Sum("valor"))["valor__sum"] or 0
        saldo = total_entradas - total_saidas
        return saldo

    def pegar_mes(self):
        hoje = timezone.now().date()
        data_inicio = date(hoje.year, hoje.month, 1)
        data_fim= hoje
        saldo=self.calcular_saldo(self,data_inicio,data_fim)
        return Saldo.objects.create(valor=saldo,mes_inicio=data_inicio,mes_fim=data_fim)
        
      

#rascunho 
#    def atualizar_saldo(self):
 #       total_entradas = Entradas.objects.aggregate(Sum("valor"))["valor__sum"] or 0
  #      total_saidas = Saidas.objects.aggregate(Sum("valor"))["valor__sum"] or 0
   #     self.valor = total_entradas - total_saidas
    #    self.save()
