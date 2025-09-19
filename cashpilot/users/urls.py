from django.urls import path
from django.contrib.auth import views as vs

urlpatterns = [
    path('login', vs.LoginView.as_view(template_name = 'users/login.html'), name='login'), 
    path('logout', vs.LogoutView.as_view(template_name = 'users/logout.html'), name='logout'),
]
