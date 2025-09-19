from django.urls import path
from django.contrib.auth import views as vs

urlparttners = [
    path('login', vs.LoginView.as_view(template_name = 'users/login.html'), name='login'), 
]
