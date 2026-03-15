from django.urls import path
from . import views

app_name = 'produtos'

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('produto/<slug:slug>/', views.detalhe_produto, name='detalhe'),
]