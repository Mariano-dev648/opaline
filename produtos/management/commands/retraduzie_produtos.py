from django.core.management.base import BaseCommand
from deep_translator import GoogleTranslator
from produtos.models import Produto
import time
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Retraduz nomes dos produtos já cadastrados para português'

    def handle(self, *args, **options):
        produtos = Produto.objects.filter(fornecedor='CJ')
        total = produtos.count()
        self.stdout.write(f'🔄 Traduzindo {total} produtos...')

        traduzidos = 0
        erros = 0

        for produto in produtos:
            try:
                nome_traduzido = GoogleTranslator(
                    source='en', target='pt'
                ).translate(produto.nome)

                produto.nome = nome_traduzido[:200]
                produto.descricao_curta = nome_traduzido[:300]
                produto.descricao = nome_traduzido
                produto.save()
                traduzidos += 1
                self.stdout.write(f'✅ {nome_traduzido[:60]}')
                time.sleep(0.5)  # evita rate limit

            except Exception as e:
                erros += 1
                logger.error(f'Erro ao traduzir {produto.nome}: {e}')
                continue

        self.stdout.write(self.style.SUCCESS(
            f'✅ Concluído! {traduzidos} traduzidos, {erros} erros.'
        ))