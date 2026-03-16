from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone
from django.contrib import messages
import mercadopago
import json
import logging
from django.conf import settings
from .models import Pagamento
from pedidos.models import Pedido

logger = logging.getLogger(__name__)


@login_required(login_url='/clientes/login/')
def pagar_pix(request, codigo):
    pedido = get_object_or_404(Pedido, codigo=codigo, cliente=request.user)

    # Verifica se já tem pagamento
    pagamento_existente = Pagamento.objects.filter(pedido=pedido).first()
    if pagamento_existente and pagamento_existente.status == 'aprovado':
        return redirect('pagamentos:sucesso', codigo=codigo)

    # Cria pagamento Pix no Mercado Pago
    sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

    dados_pix = {
        "transaction_amount": float(pedido.total),
        "description": f"Opaline — Pedido #{str(pedido.codigo)[:8].upper()}",
        "payment_method_id": "pix",
        "payer": {
            "email": pedido.cliente.email,
            "first_name": pedido.cliente.first_name,
            "last_name": pedido.cliente.last_name,
        }
    }

    resultado = sdk.payment().create(dados_pix)
    resposta = resultado.get("response", {})

    if resultado.get("status") == 201:
        pix_data = resposta.get("point_of_interaction", {}).get("transaction_data", {})

        pagamento, _ = Pagamento.objects.update_or_create(
            pedido=pedido,
            defaults={
                'metodo': 'pix',
                'status': 'pendente',
                'mp_payment_id': str(resposta.get("id", "")),
                'mp_status': resposta.get("status", ""),
                'pix_qr_code': pix_data.get("qr_code_base64", ""),
                'pix_copia_cola': pix_data.get("qr_code", ""),
                'pix_expiracao': timezone.now() + timezone.timedelta(minutes=30),
                'valor': pedido.total,
                'resposta_mp': resposta,
            }
        )

        return render(request, 'pagar_pix.html', {
            'pedido': pedido,
            'pagamento': pagamento,
        })

    logger.error(f"Erro MP: {resposta}")
    messages.error(request, 'Erro ao gerar Pix. Tente novamente.')
    return redirect('pedidos:checkout')


@csrf_exempt
def webhook_mp(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            if dados.get('type') == 'payment':
                payment_id = dados['data']['id']
                sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
                resultado = sdk.payment().get(payment_id)
                pagamento_mp = resultado.get("response", {})
                status_mp = pagamento_mp.get("status")

                pagamento = Pagamento.objects.filter(
                    mp_payment_id=str(payment_id)
                ).first()

                if pagamento:
                    if status_mp == 'approved':
                        pagamento.status = 'aprovado'
                        pagamento.pedido.status = 'pagamento_confirmado'
                        pagamento.pedido.save()
                    elif status_mp in ['cancelled', 'rejected']:
                        pagamento.status = 'recusado'
                        pagamento.pedido.status = 'cancelado'
                        pagamento.pedido.save()

                    pagamento.mp_status = status_mp
                    pagamento.save()
                    logger.info(f"Webhook processado: pagamento {payment_id} → {status_mp}")

        except Exception as e:
            logger.error(f"Erro no webhook: {e}")

    return HttpResponse(status=200)


@login_required(login_url='/clientes/login/')
def sucesso(request, codigo):
    pedido = get_object_or_404(Pedido, codigo=codigo, cliente=request.user)
    return render(request, 'sucesso.html', {'pedido': pedido})