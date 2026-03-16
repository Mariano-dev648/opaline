from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .carrinho import Carrinho
from .models import Pedido, ItemPedido
from produtos.models import Produto
from clientes.models import Endereco


def carrinho(request):
    carrinho = Carrinho(request)
    return render(request, 'carrinho.html', {'carrinho': carrinho})


def adicionar_carrinho(request, produto_id):
    carrinho = Carrinho(request)
    produto = get_object_or_404(Produto, id=produto_id, ativo=True)
    quantidade = int(request.POST.get('quantidade', 1))
    carrinho.adicionar(produto, quantidade)
    messages.success(request, f'"{produto.nome}" adicionado ao carrinho! 🛍️')
    return redirect('pedidos:carrinho')


def remover_carrinho(request, produto_id):
    carrinho = Carrinho(request)
    carrinho.remover(produto_id)
    return redirect('pedidos:carrinho')


def atualizar_carrinho(request, produto_id):
    carrinho = Carrinho(request)
    quantidade = int(request.POST.get('quantidade', 1))
    carrinho.atualizar(produto_id, quantidade)
    return redirect('pedidos:carrinho')


@login_required(login_url='/clientes/login/')
def checkout(request):
    carrinho = Carrinho(request)
    if len(carrinho) == 0:
        messages.warning(request, 'Seu carrinho está vazio.')
        return redirect('pedidos:carrinho')
    enderecos = Endereco.objects.filter(cliente=request.user)
    return render(request, 'checkout.html', {
        'carrinho': carrinho,
        'enderecos': enderecos,
    })


@login_required(login_url='/clientes/login/')
def finalizar_pedido(request):
    if request.method != 'POST':
        return redirect('pedidos:checkout')

    carrinho = Carrinho(request)
    if len(carrinho) == 0:
        return redirect('pedidos:carrinho')

    # Busca ou cria endereço
    endereco_id = request.POST.get('endereco_id')
    if endereco_id:
        endereco = get_object_or_404(Endereco, id=endereco_id, cliente=request.user)
    else:
        endereco = Endereco.objects.create(
            cliente=request.user,
            nome_destinatario=request.POST.get('nome_destinatario'),
            cep=request.POST.get('cep'),
            logradouro=request.POST.get('logradouro'),
            numero=request.POST.get('numero'),
            complemento=request.POST.get('complemento', ''),
            bairro=request.POST.get('bairro'),
            cidade=request.POST.get('cidade'),
            estado=request.POST.get('estado'),
        )

    # Cria o pedido
    pedido = Pedido.objects.create(
        cliente=request.user,
        endereco_entrega=endereco,
        subtotal=carrinho.total,
        frete=0,
        desconto=0,
        total=carrinho.total,
    )

    # Cria os itens
    for item in carrinho:
        produto = get_object_or_404(Produto, slug=item['slug'])
        ItemPedido.objects.create(
            pedido=pedido,
            produto=produto,
            quantidade=item['quantidade'],
            preco_unitario=item['preco'],
            preco_custo=item['preco_custo'],
        )

    return redirect('pagamentos:pagar_pix', codigo=pedido.codigo)



@login_required(login_url='/clientes/login/')
def confirmacao(request, codigo):
    pedido = get_object_or_404(Pedido, codigo=codigo, cliente=request.user)
    return render(request, 'confirmacao.html', {'pedido': pedido})


@login_required(login_url='/clientes/login/')
def meus_pedidos(request):
    pedidos = Pedido.objects.filter(cliente=request.user).order_by('-criado_em')
    return render(request, 'meus_pedidos.html', {'pedidos': pedidos})