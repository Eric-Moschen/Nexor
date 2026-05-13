from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.estoque.models import CategoriaProduto, Produto, UnidadeMedida


@pytest.fixture
def api_client(db):
    user = User.objects.create_user(username="estoque", password="test12345", role=User.Role.ESTOQUE)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def produto(db):
    categoria = CategoriaProduto.objects.create(nome="Produto acabado")
    unidade = UnidadeMedida.objects.create(sigla="UN", nome="Unidade")
    return Produto.objects.create(
        codigo_interno="PA-001",
        sku="PA-SKU-001",
        nome="Porta de vidro",
        categoria=categoria,
        unidade_medida=unidade,
        estoque_minimo=Decimal("1.0000"),
    )


@pytest.mark.django_db
def test_crud_produto_create(api_client):
    categoria = CategoriaProduto.objects.create(nome="Insumos")
    unidade = UnidadeMedida.objects.create(sigla="KG", nome="Quilograma")

    response = api_client.post(
        "/api/v1/estoque/produtos/",
        {
            "codigo_interno": "INS-001",
            "sku": "INS-SKU-001",
            "nome": "Silicone estrutural",
            "categoria": categoria.id,
            "unidade_medida": unidade.id,
            "estoque_minimo": "0.0000",
            "custo_medio": "10.5000",
            "preco_venda": "18.90",
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["success"] is True
    assert response.data["data"]["sku"] == "INS-SKU-001"


@pytest.mark.django_db
def test_movimentacao_entrada_api(api_client, produto):
    response = api_client.post(
        "/api/v1/estoque/movimentacoes/entrada/",
        {"produto": produto.id, "quantidade": "6.0000", "observacao": "Compra inicial"},
        format="json",
    )
    produto.refresh_from_db()

    assert response.status_code == 201
    assert response.data["success"] is True
    assert produto.estoque_atual == Decimal("6.0000")


@pytest.mark.django_db
def test_movimentacao_saida_sem_saldo_retorna_erro(api_client, produto):
    response = api_client.post(
        "/api/v1/estoque/movimentacoes/saida/",
        {"produto": produto.id, "quantidade": "6.0000"},
        format="json",
    )

    assert response.status_code == 400
    assert response.data["success"] is False
