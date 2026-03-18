from django.contrib import admin
from .models import Categoria, Produto, ImagemProduto


class ImagemProdutoInline(admin.TabularInline):
    model = ImagemProduto
    extra = 3


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']
    list_filter = ['ativo']
    search_fields = ['nome']
    prepopulated_fields = {'slug': ('nome',)}


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco_custo', 'preco_venda', 'ativo', 'destaque', 'fornecedor']
    list_filter = ['ativo', 'destaque', 'mais_vendido', 'categoria', 'fornecedor']
    search_fields = ['nome']
    prepopulated_fields = {'slug': ('nome',)}
    inlines = [ImagemProdutoInline]


@admin.register(ImagemProduto)
class ImagemProdutoAdmin(admin.ModelAdmin):
    list_display = ['produto', 'ordem']