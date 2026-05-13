from apps.fiscal.models import ClienteFiscal, EmpresaFiscal, EventoFiscal, FornecedorFiscal, NaturezaOperacao, NotaFiscal, ProdutoFiscal


def listar_empresas():
    return EmpresaFiscal.objects.filter(is_active=True).order_by("razao_social")


def listar_clientes_fiscais():
    return ClienteFiscal.objects.select_related("cliente").filter(is_active=True).order_by("cliente__razao_social")


def listar_fornecedores_fiscais():
    return FornecedorFiscal.objects.select_related("fornecedor").filter(is_active=True).order_by("fornecedor__razao_social")


def listar_produtos_fiscais():
    return ProdutoFiscal.objects.select_related("produto").filter(is_active=True).order_by("produto__nome")


def listar_naturezas_operacao():
    return NaturezaOperacao.objects.filter(is_active=True).order_by("codigo")


def listar_notas_fiscais():
    return (
        NotaFiscal.objects.select_related(
            "emitente",
            "natureza_operacao",
            "destinatario_cliente",
            "destinatario_fornecedor",
            "categoria_financeira",
            "centro_custo",
            "usuario_responsavel",
        )
        .prefetch_related("itens", "eventos")
        .filter(is_active=True)
        .order_by("-data_emissao", "-id")
    )


def listar_eventos_fiscais(nota_id):
    return EventoFiscal.objects.filter(nota_fiscal_id=nota_id).order_by("-data_evento", "-id")
