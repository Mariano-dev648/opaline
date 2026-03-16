from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
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

    pagamento_existente = Pagamento.objects.filter(pedido=pedido).first()
    if pagamento_existente and pagamento_existente.status == 'aprovado':
        return redirect('pagamentos:sucesso', codigo=codigo)

    sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title": f"Opaline — Pedido #{str(pedido.codigo)[:8].upper()}",
                "quantity": 1,
                "unit_price": float(pedido.total),
                "currency_id": "BRL",
            }
        ],
        "payer": {
            "email": pedido.cliente.email,
        },
        "back_urls": {
            "success": f"https://unpraising-fussily-ariella.ngrok-free.dev/pagamentos/sucesso/{pedido.codigo}/",
            "failure": f"https://unpraising-fussily-ariella.ngrok-free.dev/pedidos/carrinho/",
            "pending": f"https://unpraising-fussily-ariella.ngrok-free.dev/pagamentos/sucesso/{pedido.codigo}/",
        },
        "auto_return": "approved",
        "payment_methods": {
            "installments": 3,
        },
    }

    resultado = sdk.preference().create(preference_data)
    resposta = resultado.get("response", {})

    if resultado.get("status") == 201:
        pagamento, _ = Pagamento.objects.update_or_create(
            pedido=pedido,
            defaults={
                'metodo': 'pix',
                'status': 'pendente',
                'mp_payment_id': resposta.get("id", ""),
                'valor': pedido.total,
                'resposta_mp': resposta,
            }
        )

        from pedidos.carrinho import Carrinho as CarrinhoSession
        CarrinhoSession(request).limpar()

        init_point = resposta.get("sandbox_init_point") or resposta.get("init_point")
        return redirect(init_point)

    logger.error(f"Erro MP: {resposta}")
    messages.error(request, 'Erro ao gerar pagamento. Tente novamente.')
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