import logging
from .client import cj_get, cj_post
from decimal import Decimal
from django.conf import settings

logger = logging.getLogger(__name__)


def buscar_produtos_cj(keyword="jewelry", page=1, page_size=20):
    """Busca produtos de bijuterias no CJ."""
    data = cj_get("/product/list", params={
        "productNameEn": keyword,
        "pageNum": page,
        "pageSize": page_size,
    })
    if data.get("result"):
        return data["data"]["list"]
    logger.error(f"Erro ao buscar produtos CJ: {data.get('message')}")
    return []


def buscar_detalhes_produto_cj(product_id):
    """Busca detalhes e variantes de um produto."""
    data = cj_get("/product/query", params={"pid": product_id})
    if data.get("result"):
        return data["data"]
    return None


def calcular_preco_venda(preco_custo):
    """Calcula preço de venda com margem de lucro."""
    margem = Decimal(str(settings.MARGEM_LUCRO))
    preco = Decimal(str(preco_custo))
    return round(preco / (1 - margem), 2)


def criar_pedido_cj(pedido):
    """
    Cria pedido no CJ após pagamento confirmado.
    pedido = instância do seu model Pedido
    """
    produtos = []
    for item in pedido.itens.all():
        if hasattr(item.produto, 'cj_variant_id') and item.produto.cj_variant_id:
            produtos.append({
                "vid": item.produto.cj_variant_id,
                "quantity": item.quantidade,
                "shippingName": "UDS",
            })

    if not produtos:
        logger.info(f"Pedido {pedido.id} não tem produtos CJ.")
        return None

    payload = {
        "orderNumber": f"OPALINE-{pedido.id}",
        "shippingZip": pedido.cep,
        "shippingCountry": "BR",
        "shippingCountryCode": "BR",
        "shippingProvince": pedido.estado,
        "shippingCity": pedido.cidade,
        "shippingAddress": pedido.endereco,
        "shippingCustomerName": pedido.cliente_nome,
        "shippingPhone": pedido.cliente_telefone,
        "products": produtos,
    }

    data = cj_post("/shopping/order/createOrderV2", payload)

    if data.get("result"):
        cj_order_id = data["data"]["orderId"]
        logger.info(f"Pedido CJ criado: {cj_order_id}")
        return cj_order_id
    else:
        logger.error(f"Erro ao criar pedido CJ: {data.get('message')}")
        return None


def rastrear_pedido_cj(cj_order_id):
    """Rastreia status de um pedido no CJ."""
    data = cj_get("/shopping/order/getOrderDetail",
                  params={"orderId": cj_order_id})
    if data.get("result"):
        return data["data"]
    return None