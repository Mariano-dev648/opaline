from decimal import Decimal


class Carrinho:
    def __init__(self, request):
        self.session = request.session
        carrinho = self.session.get('carrinho')
        if not carrinho:
            carrinho = self.session['carrinho'] = {}
        self.carrinho = carrinho

    def adicionar(self, produto, quantidade=1):
        produto_id = str(produto.id)
        if produto_id not in self.carrinho:
            self.carrinho[produto_id] = {
                'id': produto.id,
                'quantidade': 0,
                'preco': str(produto.preco_atual),
                'preco_custo': str(produto.preco_custo),
                'nome': produto.nome,
                'slug': produto.slug,
                'imagem': produto.imagem_principal.url if produto.imagem_principal else (produto.cj_imagem_url or ''),
            }
        self.carrinho[produto_id]['quantidade'] += quantidade
        self.salvar()

    def remover(self, produto_id):
        produto_id = str(produto_id)
        if produto_id in self.carrinho:
            del self.carrinho[produto_id]
            self.salvar()

    def atualizar(self, produto_id, quantidade):
        produto_id = str(produto_id)
        if produto_id in self.carrinho:
            if quantidade <= 0:
                self.remover(produto_id)
            else:
                self.carrinho[produto_id]['quantidade'] = quantidade
                self.salvar()

    def salvar(self):
        self.session.modified = True

    def limpar(self):
        del self.session['carrinho']
        self.session.modified = True

    def __iter__(self):
        for produto_id, item in self.carrinho.items():
            item['preco'] = Decimal(item['preco'])
            item['subtotal'] = item['preco'] * item['quantidade']
            item['produto_id'] = produto_id
            yield item

    def __len__(self):
        return sum(item['quantidade'] for item in self.carrinho.values())

    @property
    def total(self):
        return sum(
            Decimal(item['preco']) * item['quantidade']
            for item in self.carrinho.values()
        )

    @property
    def total_custo(self):
        return sum(
            Decimal(item['preco_custo']) * item['quantidade']
            for item in self.carrinho.values()
        )

    @property
    def lucro_estimado(self):
        return self.total - self.total_custo