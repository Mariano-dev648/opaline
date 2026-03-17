from django.core.management.base import BaseCommand
from django.utils.text import slugify
from decimal import Decimal
from cj.client import cj_get, get_cj_token
from produtos.models import Produto, Categoria
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sincroniza produtos do CJdropshipping com o catálogo'

    def add_arguments(self, parser):
        parser.add_argument('--keyword', type=str, default='jewelry necklace',
                          help='Palavra-chave para buscar produtos')
        parser.add_argument('--paginas', type=int, default=2,
                          help='Número de páginas para sincronizar')
        parser.add_argument('--margem', type=float, default=0.40,
                          help='Margem de lucro (0.40 = 40%)')

    def handle(self, *args, **options):
        keyword = options['keyword']
        paginas = options['paginas']
        margem = Decimal(str(options['margem']))

        self.stdout.write(f'🔍 Buscando produtos: "{keyword}"...')

        # Pega ou cria categoria padrão
        categoria, _ = Categoria.objects.get_or_create(
            slug='importados',
            defaults={
                'nome': 'Importados',
                'descricao': 'Produtos importados via CJdropshipping',
                'ativo': True,
            }
        )

        criados = 0
        atualizados = 0

        for pagina in range(1, paginas + 1):
            self.stdout.write(f'📄 Página {pagina}/{paginas}...')

            data = cj_get("/product/list", params={
                "productNameEn": keyword,
                "pageNum": pagina,
                "pageSize": 20,
            })

            if not data.get("result"):
                self.stdout.write(self.style.ERROR(
                    f'Erro: {data.get("message")}'))
                break

            produtos_cj = data["data"]["list"]

            for p in produtos_cj:
                try:
                    preco_raw = p.get('sellPrice') or p.get('productPrice') or '0'
                    preco_custo = Decimal(str(preco_raw))
                    if preco_custo <= 0:
                       continue

                    # Calcula preço de venda com margem
                    preco_venda = round(preco_custo / (1 - margem), 2)

                    # Converte para BRL (aproximado)
                    DOLAR = Decimal('5.80')
                    preco_custo_brl = round(preco_custo * DOLAR, 2)
                    preco_venda_brl = round(preco_venda * DOLAR, 2)

                    nome = p.get('productNameEn', '')[:200]
                    cj_id = p.get('pid', '')
                    imagem_url = p.get('productImage', '')

                    # Gera slug único
                    slug_base = slugify(nome)[:180]
                    slug = slug_base
                    contador = 1
                    while Produto.objects.filter(slug=slug).exclude(
                            cj_product_id=cj_id).exists():
                        slug = f"{slug_base}-{contador}"
                        contador += 1

                    produto, criado = Produto.objects.update_or_create(
                        cj_product_id=cj_id,
                        defaults={
                            'nome': nome,
                            'slug': slug,
                            'descricao': p.get('productNameEn', ''),
                            'descricao_curta': nome[:300],
                            'categoria': categoria,
                            'preco_custo': preco_custo_brl,
                            'preco_venda': preco_venda_brl,
                            'codigo_fornecedor': cj_id,
                            'cj_imagem_url': imagem_url,
                            'fornecedor': 'CJ',
                            'ativo': True,
                        }
                    )

                    if criado:
                        criados += 1
                    else:
                        atualizados += 1

                except Exception as e:
                    logger.error(f"Erro ao processar produto {p.get('pid')}: {e}")
                    continue

        self.stdout.write(self.style.SUCCESS(
            f'✅ Sincronização concluída! '
            f'{criados} criados, {atualizados} atualizados.'
        ))