from django.contrib import admin
from django.utils.html import format_html
from .models import Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['preco_unitario', 'preco_custo']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['codigo_curto', 'cliente', 'status_display', 'total', 'enviado_ao_fornecedor', 'criado_em']
    list_filter = ['status', 'enviado_ao_fornecedor']
    search_fields = ['codigo', 'cliente__email']
    readonly_fields = ['codigo', 'criado_em', 'atualizado_em']
    inlines = [ItemPedidoInline]

    def codigo_curto(self, obj):
        return str(obj.codigo)[:8].upper()
    codigo_curto.short_description = 'Código'

    def status_display(self, obj):
        cores = {
            'aguardando_pagamento': '#f39c12',
            'pagamento_confirmado': '#27ae60',
            'enviado_fornecedor':   '#2980b9',
            'em_transito':         '#8e44ad',
            'entregue':            '#27ae60',
            'cancelado':           '#e74c3c',
            'reembolsado':         '#7f8c8d',
        }
        cor = cores.get(obj.status, '#333')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            cor, obj.get_status_display()
        )
    status_display.short_description = 'Status'