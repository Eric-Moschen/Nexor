from apps.fornecedores.models import Fornecedor


def criar_fornecedor(*, razao_social, documento, nome_fantasia="", email="", telefone="", created_by=None):
    return Fornecedor.objects.create(
        razao_social=razao_social,
        nome_fantasia=nome_fantasia,
        documento=documento,
        email=email,
        telefone=telefone,
        created_by=created_by,
        updated_by=created_by,
    )
