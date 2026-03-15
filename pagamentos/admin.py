from django.contrib import admin
from .models import Pagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'metodo', 'status', 'valor', 'criado_em']
    list_filter = ['status', 'metodo']
    readonly_fields = ['mp_payment_id', 'pix_qr_code', 'pix_copia_cola', 'resposta_mp']