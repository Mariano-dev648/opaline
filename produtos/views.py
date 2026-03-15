from django.shortcuts import render
from .models import Produto, Categoria

def home(request):
    destaques = Produto.objects.filter(ativo=True, destaque=True)[:8]
    mais_vendidos = Produto.objects.filter(ativo=True, mais_vendido=True)[:4]
    categorias = Categoria.objects.filter(ativo=True)
    return render(request, 'home.html', {
        'destaques': destaques,
        'mais_vendidos': mais_vendidos,
        'categorias': categorias,
    })

def catalogo(request):
    produtos = Produto.objects.filter(ativo=True)
    categorias = Categoria.objects.filter(ativo=True)
    return render(request, 'catalogo.html', {
        'produtos': produtos,
        'categorias': categorias,
    })

def detalhe_produto(request, slug):
    from django.shortcuts import get_object_or_404
    produto = get_object_or_404(Produto, slug=slug, ativo=True)
    return render(request, 'detalhe_produto.html', {'produto': produto})