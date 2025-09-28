from django.contrib import admin
from .models import Entradas, Saidas, Saldo
# Register your models here.
admin.site.register(Entradas)
admin.site.register(Saidas)
admin.site.register(Saldo)