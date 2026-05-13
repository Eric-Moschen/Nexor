from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.estoque.models import CategoriaProduto, Produto, UnidadeMedida


@pytest.fixture
def api_client(db):
    user = User.objects.create_user(username="compras-api", password="test12345", role=User.Role.COMPRAS)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def produto(db):
    categoria = CategoriaProduto.objects.create(nome="Materia prima compras")
    unidade = UnidadeMedida.objects.create(sigla="CX", nome="Caixa")
    return Produto.objects.create(
        codigo_interno="CMP-001",
        sku="CMP-SKU-001",
        nome="Parafuso inox",
        categoria=categoria,
        unidade_medida=unidade,
    )


@pytest.mark.django_db
def test_criar_solicitacao_api(api_client, produto):
    response = api_client.post(
        "/api/v1/compras/solicitacoes/",
        {
            "centro_custo": "Producao",
            "justificativa": "Reposicao",
            "prioridade": "media",
            "itens": [{
                "produto": produto.id,
                "quantidade_solicitada": "2.0000",
                "unidade_medida": produto.unidade_medida_id,
            }],
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["success"] is True
    assert response.data["data"]["itens"][0]["quantidade_solicitada"] == "2.0000"


@pytest.mark.django_db
def test_bloquear_solicitacao_sem_itens_api(api_client):
    response = api_client.post(
        "/api/v1/compras/solicitacoes/",
        {
            "centro_custo": "Producao",
            "justificativa": "Reposicao",
            "prioridade": "media",
            "itens": [],
        },
        format="json",
    )

    assert response.status_code == 400
