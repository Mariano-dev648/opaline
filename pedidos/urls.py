from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('carrinho/', views.carrinho, name='carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('confirmacao/<uuid:codigo>/', views.confirmacao, name='confirmacao'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
]