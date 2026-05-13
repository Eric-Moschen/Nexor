from apps.estoque.models import CategoriaProduto, MovimentacaoEstoque, Produto, UnidadeMedida


def listar_categorias():
    return CategoriaProduto.objects.filter(is_active=True).order_by("nome")


def listar_unidades_medida():
    return UnidadeMedida.objects.filter(is_active=True).order_by("sigla")


def listar_produtos():
    return (
        Produto.objects.select_related("categoria", "unidade_medida")
        .filter(is_active=True)
        .order_by("nome")
    )


def listar_movimentacoes():
    return (
        MovimentacaoEstoque.objects.select_related("produto", "usuario_responsavel")
        .all()
        .order_by("-data_movimentacao", "-id")
    )


def obter_produto_para_movimentacao(produto_id):
    return Produto.objects.select_for_update().get(id=produto_id, is_active=True)
