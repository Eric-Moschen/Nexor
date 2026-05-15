from django.core.management import call_command
from django.core.management.base import BaseCommand

from apps.financeiro.enums import TipoFinanceiro
from apps.financeiro.models import CategoriaFinanceira, CentroCusto
from apps.fiscal.models import NaturezaOperacao


class Command(BaseCommand):
    help = "Executa seeds corporativos iniciais do Nexor ERP."

    def add_arguments(self, parser):
        parser.add_argument("--admin-email", default="admin@nexor.local")
        parser.add_argument("--admin-username", default="admin")
        parser.add_argument("--admin-password", default="Admin@12345")

    def handle(self, *args, **options):
        call_command(
            "seed_rbac",
            admin_email=options["admin_email"],
            admin_username=options["admin_username"],
            admin_password=options["admin_password"],
        )
        self._seed_financeiro()
        self._seed_fiscal()
        self.stdout.write(self.style.SUCCESS("Seeds iniciais do Nexor ERP executados com sucesso."))

    def _seed_financeiro(self):
        for codigo, nome in [
            ("ADM", "Administrativo"),
            ("COM", "Comercial"),
            ("COMP", "Compras"),
            ("OPER", "Operacional"),
            ("PROD", "Producao"),
        ]:
            CentroCusto.objects.update_or_create(codigo=codigo, defaults={"nome": nome, "is_active": True})

        for nome, tipo in [
            ("Vendas", TipoFinanceiro.RECEITA),
            ("Servicos", TipoFinanceiro.RECEITA),
            ("Materia prima", TipoFinanceiro.DESPESA),
            ("Manutencao", TipoFinanceiro.DESPESA),
            ("Administrativo", TipoFinanceiro.DESPESA),
        ]:
            CategoriaFinanceira.objects.update_or_create(nome=nome, tipo=tipo, defaults={"is_active": True})

    def _seed_fiscal(self):
        for seed in [
            {"codigo": "VENDA-5102", "descricao": "Venda de mercadoria adquirida de terceiros", "tipo_operacao": "venda", "cfop_padrao": "5102", "movimenta_estoque": True, "gera_financeiro": True},
            {"codigo": "COMPRA-1102", "descricao": "Compra para comercializacao", "tipo_operacao": "compra", "cfop_padrao": "1102", "movimenta_estoque": True, "gera_financeiro": True},
            {"codigo": "SERVICO-5933", "descricao": "Prestacao de servico tributado", "tipo_operacao": "venda", "cfop_padrao": "5933", "movimenta_estoque": False, "gera_financeiro": True},
        ]:
            NaturezaOperacao.objects.update_or_create(codigo=seed["codigo"], defaults={**seed, "is_active": True})
