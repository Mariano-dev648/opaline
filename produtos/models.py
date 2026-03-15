from django.db import models

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(upload_to='categorias/', blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    # Identificação
    nome = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    descricao = models.TextField()
    descricao_curta = models.CharField(max_length=300)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='produtos')

    # Preços
    preco_custo = models.DecimalField(max_digits=10, decimal_places=2)   # preço do fornecedor
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)   # preço no site
    preco_promocional = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Dropshipping — código do produto no fornecedor
    codigo_fornecedor = models.CharField(max_length=100, unique=True)
    url_fornecedor = models.URLField(blank=True)

    # Imagens
    imagem_principal = models.ImageField(upload_to='produtos/')
    
    # Detalhes
    material = models.CharField(max_length=100, blank=True)  # ex: folheado a ouro 18k
    peso = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    dimensoes = models.CharField(max_length=100, blank=True)

    # Controle
    ativo = models.BooleanField(default=True)
    destaque = models.BooleanField(default=False)
    mais_vendido = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-criado_em']

    def __str__(self):
        return self.nome

    @property
    def margem_lucro(self):
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_venda) * 100
        return 0

    @property
    def preco_atual(self):
        if self.preco_promocional:
            return self.preco_promocional
        return self.preco_venda


class ImagemProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='imagens')
    imagem = models.ImageField(upload_to='produtos/galeria/')
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f'Imagem {self.ordem} — {self.produto.nome}'






