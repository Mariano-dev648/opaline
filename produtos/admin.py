from django.contrib import admin
from django.utils.html import format_html
from .models import Categoria, Produto, ImagemProduto

class ImagemProdutoInline(admin.TabularInline):
    model =ImagemProduto
    extra =3

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativo', 'criado_em']
    list_filter = ['ativo']
    search_fields = ['nome']
    prepopulated_fields ={'slug': ('nome',)}

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco_custo', 'preco_venda', 'margem_display', 'ativo', 'destaque']
    list_filter = ['ativo', 'destaque', 'mais_vendido', 'categoria']
    search_fields = ['nome', 'categoria_fornecedor']
    prepopulated_fields = {'slug': ('nome',)}
    inlines = [ImagemProdutoInline]
    reandonly_fields = ['margem_display']

    def margem_display(self, obj):
        margem = float(obj.margem_lucro)
        cor = '#27ae60' if margem >= 35 else '#e74c3c'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{:.1f}%</span>',
            cor, margem
        )
    margem_display.short_description = 'Margem de Lucro'