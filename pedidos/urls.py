from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:produto_id>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/atualizar/<int:produto_id>/', views.atualizar_carrinho, name='atualizar_carrinho'),
    path('checkout/', views.checkout, name='checkout'),
    path('finalizar/', views.finalizar_pedido, name='finalizar_pedido'),
    path('confirmacao/<uuid:codigo>/', views.confirmacao, name='confirmacao'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
]