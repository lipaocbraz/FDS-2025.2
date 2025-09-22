from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('entradas/',views.entradas_view,name='entradas'),
    path('saidas/',views.saidas_view,name='saidas'),
]