from django.urls import path
from django.contrib.auth import views as vs
from . import views

urlpatterns = [
    path('login', vs.LoginView.as_view(template_name = 'users/html/login.html'), name='login'), 
    path('logout', views.logout_view, name='logout'),
    path('cadastro',views.cadastro, name='cadastro'),
]
