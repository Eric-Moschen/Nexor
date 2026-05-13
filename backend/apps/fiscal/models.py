from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.clientes.models import Cliente
from apps.core.models import AuditModel, SoftDeleteModel, TimeStampedModel
from apps.estoque.models import Produto
from apps.financeiro.models import CategoriaFinanceira, CentroCusto, ContaPagar, ContaReceber
from apps.fiscal.enums import AmbienteFiscal, RegimeTributario, StatusNFe, TipoEventoFiscal, TipoOperacao
from apps.fornecedores.models import Fornecedor


class EmpresaFiscal(TimeStampedModel, SoftDeleteModel, AuditModel):
    razao_social = models.CharField(max_length=180)
    nome_fantasia = models.CharField(max_length=180, blank=True)
    cnpj = models.CharField(max_length=14, unique=True, db_index=True)
    inscricao_estadual = models.CharField(max_length=30, blank=True)
    inscricao_municipal = models.CharField(max_length=30, blank=True)
    regime_tributario = models.CharField(max_length=30, choices=RegimeTributario.choices)
    cnae = models.CharField(max_length=20, blank=True)
    endereco_fiscal = models.TextField()
    municipio_ibge = models.CharField(max_length=7)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    certificado_a1 = models.FileField(upload_to="certificados/", blank=True)
    certificado_senha_protegida = models.TextField(blank=True)
    ambiente = models.CharField(max_length=20, choices=AmbienteFiscal.choices, default=AmbienteFiscal.HOMOLOGACAO)

    class Meta:
        ordering = ["razao_social"]

    def __str__(self):
        return self.razao_social


class ClienteFiscal(TimeStampedModel, SoftDeleteModel, AuditModel):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE, related_name="dados_fiscais")
    cpf_cnpj = models.CharField(max_length=14, db_index=True)
    inscricao_estadual = models.CharField(max_length=30, blank=True)
    indicador_ie = models.CharField(max_length=30, default="nao_contribuinte")
    endereco_fiscal = models.TextField()
    municipio_ibge = models.CharField(max_length=7)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    email_fiscal = models.EmailField(blank=True)

    def __str__(self):
        return self.cliente.razao_social


class FornecedorFiscal(TimeStampedModel, SoftDeleteModel, AuditModel):
    fornecedor = models.OneToOneField(Fornecedor, on_delete=models.CASCADE, related_name="dados_fiscais")
    cpf_cnpj = models.CharField(max_length=14, db_index=True)
    inscricao_estadual = models.CharField(max_length=30, blank=True)
    indicador_ie = models.CharField(max_length=30, default="nao_contribuinte")
    endereco_fiscal = models.TextField()
    municipio_ibge = models.CharField(max_length=7)
    uf = models.CharField(max_length=2)
    cep = models.CharField(max_length=8)
    email_fiscal = models.EmailField(blank=True)

    def __str__(self):
        return self.fornecedor.razao_social


class ProdutoFiscal(TimeStampedModel, SoftDeleteModel, AuditModel):
    produto = models.OneToOneField(Produto, on_delete=models.CASCADE, related_name="dados_fiscais")
    ncm = models.CharField(max_length=8, db_index=True)
    cest = models.CharField(max_length=7, blank=True)
    cfop_padrao = models.CharField(max_length=4)
    unidade_comercial = models.CharField(max_length=10)
    unidade_tributavel = models.CharField(max_length=10)
    origem_mercadoria = models.CharField(max_length=1, default="0")
    cst_csosn = models.CharField(max_length=4)
    aliquota_icms = models.DecimalField(max_digits=7, decimal_places=4, default=Decimal("0.0000"), validators=[MinValueValidator(Decimal("0"))])
    aliquota_pis = models.DecimalField(max_digits=7, decimal_places=4, default=Decimal("0.0000"), validators=[MinValueValidator(Decimal("0"))])
    aliquota_cofins = models.DecimalField(max_digits=7, decimal_places=4, default=Decimal("0.0000"), validators=[MinValueValidator(Decimal("0"))])
    aliquota_ipi = models.DecimalField(max_digits=7, decimal_places=4, default=Decimal("0.0000"), validators=[MinValueValidator(Decimal("0"))])

    def __str__(self):
        return self.produto.nome


class NaturezaOperacao(TimeStampedModel, SoftDeleteModel, AuditModel):
    codigo = models.CharField(max_length=20, unique=True, db_index=True)
    descricao = models.CharField(max_length=180)
    tipo_operacao = models.CharField(max_length=20, choices=TipoOperacao.choices, db_index=True)
    cfop_padrao = models.CharField(max_length=4)
    movimenta_estoque = models.BooleanField(default=True)
    gera_financeiro = models.BooleanField(default=True)

    class Meta:
        ordering = ["codigo"]

    def __str__(self):
        return self.descricao


class NotaFiscal(TimeStampedModel, SoftDeleteModel, AuditModel):
    numero = models.PositiveIntegerField()
    serie = models.PositiveIntegerField(default=1)
    chave_acesso = models.CharField(max_length=44, blank=True, db_index=True)
    protocolo = models.CharField(max_length=60, blank=True)
    ambiente = models.CharField(max_length=20, choices=AmbienteFiscal.choices, default=AmbienteFiscal.HOMOLOGACAO)
    tipo_emissao = models.CharField(max_length=30, default="normal")
    tipo_operacao = models.CharField(max_length=20, choices=TipoOperacao.choices)
    natureza_operacao = models.ForeignKey(NaturezaOperacao, on_delete=models.PROTECT, related_name="notas_fiscais")
    emitente = models.ForeignKey(EmpresaFiscal, on_delete=models.PROTECT, related_name="notas_emitidas")
    destinatario_cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.PROTECT, related_name="notas_fiscais")
    destinatario_fornecedor = models.ForeignKey(Fornecedor, null=True, blank=True, on_delete=models.PROTECT, related_name="notas_fiscais")
    data_emissao = models.DateTimeField(auto_now_add=True)
    data_saida_entrada = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=StatusNFe.choices, default=StatusNFe.RASCUNHO, db_index=True)
    valor_produtos = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    valor_frete = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    valor_desconto = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    valor_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    xml_autorizado = models.TextField(blank=True)
    xml_cancelamento = models.TextField(blank=True)
    danfe_pdf = models.FileField(upload_to="danfes/", blank=True)
    motivo_rejeicao = models.TextField(blank=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="notas_fiscais")
    conta_receber = models.ForeignKey(ContaReceber, null=True, blank=True, on_delete=models.PROTECT, related_name="notas_fiscais")
    conta_pagar = models.ForeignKey(ContaPagar, null=True, blank=True, on_delete=models.PROTECT, related_name="notas_fiscais")
    categoria_financeira = models.ForeignKey(CategoriaFinanceira, null=True, blank=True, on_delete=models.PROTECT, related_name="notas_fiscais")
    centro_custo = models.ForeignKey(CentroCusto, null=True, blank=True, on_delete=models.PROTECT, related_name="notas_fiscais")

    class Meta:
        ordering = ["-data_emissao", "-id"]
        constraints = [
            models.UniqueConstraint(fields=["numero", "serie", "emitente", "ambiente"], name="fiscal_nfe_numero_serie_emitente_ambiente_uniq"),
            models.CheckConstraint(check=models.Q(valor_frete__gte=0), name="fiscal_nfe_frete_gte_0"),
            models.CheckConstraint(check=models.Q(valor_desconto__gte=0), name="fiscal_nfe_desconto_gte_0"),
        ]
        indexes = [
            models.Index(fields=["status", "data_emissao"]),
            models.Index(fields=["chave_acesso"]),
        ]

    def __str__(self):
        return f"NFe {self.numero}/{self.serie}"


class ItemNotaFiscal(TimeStampedModel):
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE, related_name="itens")
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, related_name="itens_nfe")
    descricao = models.CharField(max_length=220)
    cfop = models.CharField(max_length=4)
    ncm = models.CharField(max_length=8)
    cst_csosn = models.CharField(max_length=4)
    quantidade = models.DecimalField(max_digits=14, decimal_places=4, validators=[MinValueValidator(Decimal("0.0001"))])
    valor_unitario = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    valor_total = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    desconto = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"), validators=[MinValueValidator(Decimal("0"))])
    base_icms = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    valor_icms = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    base_pis = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    valor_pis = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    base_cofins = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    valor_cofins = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    base_ipi = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))
    valor_ipi = models.DecimalField(max_digits=14, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(check=models.Q(quantidade__gt=0), name="fiscal_item_quantidade_gt_0"),
            models.CheckConstraint(check=models.Q(valor_unitario__gte=0), name="fiscal_item_valor_unit_gte_0"),
        ]


class EventoFiscal(TimeStampedModel):
    nota_fiscal = models.ForeignKey(NotaFiscal, on_delete=models.CASCADE, related_name="eventos")
    tipo_evento = models.CharField(max_length=30, choices=TipoEventoFiscal.choices, db_index=True)
    codigo_retorno = models.CharField(max_length=20, blank=True)
    mensagem = models.TextField()
    protocolo = models.CharField(max_length=60, blank=True)
    xml_retorno = models.TextField(blank=True)
    data_evento = models.DateTimeField(auto_now_add=True, db_index=True)
    usuario_responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["-data_evento", "-id"]
        indexes = [models.Index(fields=["nota_fiscal", "tipo_evento"])]
