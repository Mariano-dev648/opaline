from django.db import models
from clientes.models import Cliente, Endereco
from produtos.models import Produto
import uuid


class Pedido(models.Model):
    STATUS = [
        ('aguardando_pagamento', '⏳ Aguardando Pagamento'),
        ('pagamento_confirmado', '✅ Pagamento Confirmado'),
        ('enviado_fornecedor',   '📦 Enviado ao Fornecedor'),
        ('em_transito',         '🚚 Em Trânsito'),
        ('entregue',            '🎉 Entregue'),
        ('cancelado',           '❌ Cancelado'),
        ('reembolsado',         '↩️ Reembolsado'),
    ]

    # Identificação única do pedido
    codigo = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='pedidos')
    endereco_entrega = models.ForeignKey(Endereco, on_delete=models.PROTECT)

    # Status e rastreio
    status = models.CharField(max_length=30, choices=STATUS, default='aguardando_pagamento')
    codigo_rastreio = models.CharField(max_length=100, blank=True)

    # Valores
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    frete = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    # Dropshipping — controle do repasse ao fornecedor
    enviado_ao_fornecedor = models.BooleanField(default=False)
    data_envio_fornecedor = models.DateTimeField(null=True, blank=True)
    numero_pedido_fornecedor = models.CharField(max_length=100, blank=True)

    # Observações
    observacoes = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-criado_em']

    def __str__(self):
        return f'Pedido #{str(self.codigo)[:8].upper()} — {self.cliente}'


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)  # preço na hora da compra
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)     # custo registrado

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f'{self.quantidade}x {self.produto.nome}'

    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade