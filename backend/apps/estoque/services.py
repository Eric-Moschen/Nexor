from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from apps.estoque.models import MovimentacaoEstoque
from apps.estoque.repositories import MovimentacaoEstoqueRepository, ProdutoRepository


class EstoqueService:
    def __init__(self, produto_repository=None, movimentacao_repository=None):
        self.produto_repository = produto_repository or ProdutoRepository()
        self.movimentacao_repository = movimentacao_repository or MovimentacaoEstoqueRepository()

    @transaction.atomic
    def registrar_entrada(self, *, produto_id, quantidade, usuario=None, observacao=""):
        return self._registrar_movimentacao(
            produto_id=produto_id,
            tipo=MovimentacaoEstoque.Tipo.ENTRADA,
            quantidade=quantidade,
            usuario=usuario,
            observacao=observacao,
        )

    @transaction.atomic
    def registrar_saida(self, *, produto_id, quantidade, usuario=None, observacao=""):
        return self._registrar_movimentacao(
            produto_id=produto_id,
            tipo=MovimentacaoEstoque.Tipo.SAIDA,
            quantidade=quantidade,
            usuario=usuario,
            observacao=observacao,
        )

    @transaction.atomic
    def registrar_ajuste(self, *, produto_id, quantidade, usuario=None, observacao=""):
        return self._registrar_movimentacao(
            produto_id=produto_id,
            tipo=MovimentacaoEstoque.Tipo.AJUSTE,
            quantidade=quantidade,
            usuario=usuario,
            observacao=observacao,
        )

    def _registrar_movimentacao(self, *, produto_id, tipo, quantidade, usuario=None, observacao=""):
        quantidade = Decimal(str(quantidade))
        if quantidade <= 0:
            raise ValidationError("A quantidade deve ser maior que zero.")

        produto = self.produto_repository.get_active_for_update(produto_id)
        saldo_anterior = produto.estoque_atual

        if tipo == MovimentacaoEstoque.Tipo.ENTRADA:
            saldo_posterior = saldo_anterior + quantidade
        elif tipo == MovimentacaoEstoque.Tipo.SAIDA:
            if saldo_anterior < quantidade:
                raise ValidationError("Saldo insuficiente para realizar a saida.")
            saldo_posterior = saldo_anterior - quantidade
        elif tipo == MovimentacaoEstoque.Tipo.AJUSTE:
            saldo_posterior = quantidade
        else:
            raise ValidationError("Tipo de movimentacao nao suportado.")

        produto.estoque_atual = saldo_posterior
        self.produto_repository.save_stock(produto)

        return self.movimentacao_repository.create(
            produto=produto,
            tipo=tipo,
            quantidade=quantidade,
            saldo_anterior=saldo_anterior,
            saldo_posterior=saldo_posterior,
            usuario_responsavel=usuario if getattr(usuario, "is_authenticated", False) else None,
            observacao=observacao,
        )
