from django.db import models
from pedidos.models import Pedido


class Pagamento(models.Model):
    STATUS = [
        ('pendente',   '⏳ Pendente'),
        ('aprovado',   '✅ Aprovado'),
        ('recusado',   '❌ Recusado'),
        ('cancelado',  '🚫 Cancelado'),
        ('reembolsado','↩️ Reembolsado'),
    ]

    METODOS = [
        ('pix',           'Pix'),
        ('cartao_credito','Cartão de Crédito'),
        ('boleto',        'Boleto'),
    ]

    pedido = models.OneToOneField(Pedido, on_delete=models.PROTECT, related_name='pagamento')
    metodo = models.CharField(max_length=20, choices=METODOS)
    status = models.CharField(max_length=15, choices=STATUS, default='pendente')

    # Dados do Mercado Pago
    mp_payment_id = models.CharField(max_length=100, blank=True)   # ID no Mercado Pago
    mp_status = models.CharField(max_length=50, blank=True)
    mp_status_detail = models.CharField(max_length=100, blank=True)

    # Pix específico
    pix_qr_code = models.TextField(blank=True)        # QR code em base64
    pix_copia_cola = models.TextField(blank=True)     # código copia e cola
    pix_expiracao = models.DateTimeField(null=True, blank=True)

    # Valores
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    # Segurança — log de respostas do MP
    resposta_mp = models.JSONField(default=dict, blank=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        return f'Pagamento {self.metodo} — {self.status} — Pedido {self.pedido.codigo}'