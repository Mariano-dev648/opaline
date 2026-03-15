// Carrinho de compras (sessão)
document.addEventListener('DOMContentLoaded', function() {
    atualizarContadorCarrinho();
});

function atualizarContadorCarrinho() {
    const carrinho = JSON.parse(localStorage.getItem('opaline_carrinho') || '[]');
    const contador = document.querySelector('.cart-count');
    if (contador) {
        contador.textContent = carrinho.reduce((total, item) => total + item.quantidade, 0);
    }
}