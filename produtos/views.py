from django.shortcuts import render, get_object_or_404
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

    # Filtro por categoria
    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        produtos = produtos.filter(categoria__slug=categoria_slug)

    # Busca por nome
    busca = request.GET.get('q')
    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    return render(request, 'catalogo.html', {
        'produtos': produtos,
        'categorias': categorias,
        'busca': busca,
    })


def detalhe_produto(request, slug):
    produto = get_object_or_404(Produto, slug=slug, ativo=True)
    relacionados = Produto.objects.filter(
        categoria=produto.categoria,
        ativo=True
    ).exclude(id=produto.id)[:4]
    return render(request, 'detalhe_produto.html', {
        'produto': produto,
        'relacionados': relacionados,
    })