from decimal import Decimal

import pytest
from django.core.exceptions import ValidationError

from apps.accounts.models import User
from apps.clientes.models import Cliente
from apps.estoque.models import CategoriaProduto, Produto, UnidadeMedida
from apps.fiscal.enums import RegimeTributario, StatusNFe, TipoOperacao
from apps.fiscal.integrations.certificate_manager import CertificateManager
from apps.fiscal.models import ClienteFiscal, EmpresaFiscal, NaturezaOperacao, ProdutoFiscal
from apps.fiscal.services import FiscalService


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="fiscal", password="test12345", role=User.Role.FISCAL)


@pytest.fixture
def empresa(usuario):
    manager = CertificateManager()
    empresa = EmpresaFiscal.objects.create(
        razao_social="Nexor Testes LTDA",
        cnpj="12345678000195",
        regime_tributario=RegimeTributario.SIMPLES,
        endereco_fiscal="Rua Central, 100",
        municipio_ibge="3550308",
        uf="SP",
        cep="01001000",
        certificado_senha_protegida=manager.protect_password("senha"),
        created_by=usuario,
        updated_by=usuario,
    )
    empresa.certificado_a1.name = "certificados/teste.pfx"
    empresa.save(update_fields=["certificado_a1"])
    return empresa


@pytest.fixture
def cliente(usuario):
    cliente = Cliente.objects.create(razao_social="Cliente Fiscal", documento="98765432000198")
    ClienteFiscal.objects.create(
        cliente=cliente,
        cpf_cnpj="98765432000198",
        endereco_fiscal="Avenida Fiscal, 10",
        municipio_ibge="3550308",
        uf="SP",
        cep="01001000",
        created_by=usuario,
        updated_by=usuario,
    )
    return cliente


@pytest.fixture
def produto(usuario):
    categoria = CategoriaProduto.objects.create(nome="Mercadorias")
    unidade = UnidadeMedida.objects.create(sigla="UN", nome="Unidade")
    produto = Produto.objects.create(
        codigo_interno="FISC-001",
        sku="FISC-SKU-001",
        nome="Produto fiscal",
        categoria=categoria,
        unidade_medida=unidade,
        estoque_atual=Decimal("10.0000"),
        preco_venda=Decimal("25.00"),
    )
    ProdutoFiscal.objects.create(
        produto=produto,
        ncm="12345678",
        cfop_padrao="5102",
        unidade_comercial="UN",
        unidade_tributavel="UN",
        cst_csosn="102",
        aliquota_icms=Decimal("18.0000"),
        created_by=usuario,
        updated_by=usuario,
    )
    return produto


@pytest.fixture
def natureza(usuario):
    return NaturezaOperacao.objects.create(
        codigo="VENDA-TESTE",
        descricao="Venda fiscal de teste",
        tipo_operacao=TipoOperacao.VENDA,
        cfop_padrao="5102",
        created_by=usuario,
        updated_by=usuario,
    )


@pytest.mark.django_db
def test_criar_nfe_calcula_totais_e_impostos(usuario, empresa, cliente, produto, natureza):
    nota = FiscalService().criar_nfe(
        usuario=usuario,
        numero=1,
        serie=1,
        tipo_operacao=TipoOperacao.VENDA,
        natureza_operacao=natureza,
        emitente=empresa,
        destinatario_cliente=cliente,
        itens=[{"produto": produto, "quantidade": Decimal("2.0000"), "valor_unitario": Decimal("25.00")}],
    )

    item = nota.itens.first()
    assert nota.status == StatusNFe.RASCUNHO
    assert nota.valor_total == Decimal("50.00")
    assert item.valor_icms == Decimal("9.00")


@pytest.mark.django_db
def test_fluxo_validar_assinar_enviar_autoriza_e_movimenta_estoque(usuario, empresa, cliente, produto, natureza):
    service = FiscalService()
    nota = service.criar_nfe(
        usuario=usuario,
        numero=2,
        serie=1,
        tipo_operacao=TipoOperacao.VENDA,
        natureza_operacao=natureza,
        emitente=empresa,
        destinatario_cliente=cliente,
        itens=[{"produto": produto, "quantidade": Decimal("3.0000"), "valor_unitario": Decimal("10.00")}],
    )

    service.validar_nfe(nota_id=nota.id, usuario=usuario)
    service.assinar_nfe(nota_id=nota.id, usuario=usuario)
    nota = service.enviar_nfe(nota_id=nota.id, usuario=usuario)
    produto.refresh_from_db()

    assert nota.status == StatusNFe.AUTORIZADA
    assert nota.protocolo
    assert produto.estoque_atual == Decimal("7.0000")


@pytest.mark.django_db
def test_assinar_bloqueia_empresa_sem_certificado(usuario, empresa, cliente, produto, natureza):
    empresa.certificado_a1 = ""
    empresa.certificado_senha_protegida = ""
    empresa.save(update_fields=["certificado_a1", "certificado_senha_protegida"])
    service = FiscalService()
    nota = service.criar_nfe(
        usuario=usuario,
        numero=3,
        serie=1,
        tipo_operacao=TipoOperacao.VENDA,
        natureza_operacao=natureza,
        emitente=empresa,
        destinatario_cliente=cliente,
        itens=[{"produto": produto, "quantidade": Decimal("1.0000"), "valor_unitario": Decimal("10.00")}],
    )
    service.validar_nfe(nota_id=nota.id, usuario=usuario)

    with pytest.raises(ValidationError):
        service.assinar_nfe(nota_id=nota.id, usuario=usuario)
