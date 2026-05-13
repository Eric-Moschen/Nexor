from apps.estoque.models import MovimentacaoEstoque, Produto


class ProdutoRepository:
    model = Produto

    def get_active_for_update(self, produto_id):
        return self.model.objects.select_for_update().get(id=produto_id, is_active=True)

    def save_stock(self, produto):
        produto.save(update_fields=["estoque_atual", "updated_at"])
        return produto


class MovimentacaoEstoqueRepository:
    model = MovimentacaoEstoque

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)
