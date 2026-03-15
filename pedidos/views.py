from django.shortcuts import render

def placeholder(request):
    return render(request, 'home.html')

carrinho = checkout = confirmacao = meus_pedidos = placeholder