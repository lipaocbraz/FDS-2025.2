from django.urls import path
from django.contrib.auth import views as vs
from . import views

urlpatterns = [
    path('login/', views.MeuLoginView.as_view(), name='login'), 
    path('logout', views.logout_view, name='logout'),
    path('cadastro',views.cadastro, name='cadastro'),
]
