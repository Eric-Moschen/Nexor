# Generated for the Prompt 07 budgets module baseline.

import decimal
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("clientes", "0001_initial"),
        ("estoque", "0001_initial"),
        ("ordens_servico", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Orcamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("numero", models.CharField(db_index=True, max_length=30, unique=True)),
                ("titulo", models.CharField(db_index=True, max_length=180)),
                ("descricao", models.TextField(blank=True)),
                ("data_criacao", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("data_validade", models.DateField(db_index=True)),
                ("status", models.CharField(choices=[("rascunho", "Rascunho"), ("em_analise", "Em analise"), ("enviado", "Enviado"), ("aprovado", "Aprovado"), ("reprovado", "Reprovado"), ("expirado", "Expirado"), ("convertido_os", "Convertido em OS"), ("cancelado", "Cancelado")], db_index=True, default="rascunho", max_length=30)),
                ("condicao_pagamento", models.CharField(blank=True, max_length=180)),
                ("prazo_entrega", models.CharField(blank=True, max_length=120)),
                ("observacoes_internas", models.TextField(blank=True)),
                ("observacoes_cliente", models.TextField(blank=True)),
                ("valor_produtos", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("valor_servicos", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("valor_desconto", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("valor_total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("custo_total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("margem_estimada", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=7)),
                ("motivo_reprovacao", models.TextField(blank=True)),
                ("pdf_gerado", models.FileField(blank=True, upload_to="orcamentos/")),
                ("cliente", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orcamentos", to="clientes.cliente")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orcamento_created", to=settings.AUTH_USER_MODEL)),
                ("ordem_servico", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="orcamento_origem", to="ordens_servico.ordemservico")),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="orcamento_updated", to=settings.AUTH_USER_MODEL)),
                ("usuario_responsavel", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orcamentos_responsavel", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-data_criacao", "-id"]},
        ),
        migrations.CreateModel(
            name="ItemProdutoOrcamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("descricao", models.CharField(max_length=220)),
                ("quantidade", models.DecimalField(decimal_places=4, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.0001"))])),
                ("custo_unitario", models.DecimalField(decimal_places=4, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("valor_unitario", models.DecimalField(decimal_places=2, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("desconto", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("valor_total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14)),
                ("custo_total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14)),
                ("orcamento", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="itens_produto", to="orcamentos.orcamento")),
                ("produto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="itens_orcamento", to="estoque.produto")),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="ItemServicoOrcamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("descricao", models.CharField(max_length=220)),
                ("quantidade", models.DecimalField(decimal_places=4, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.0001"))])),
                ("custo_estimado", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("valor_unitario", models.DecimalField(decimal_places=2, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("desconto", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("valor_total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14)),
                ("observacao", models.TextField(blank=True)),
                ("orcamento", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="itens_servico", to="orcamentos.orcamento")),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="HistoricoOrcamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("tipo_evento", models.CharField(choices=[("criacao", "Criacao"), ("alteracao", "Alteracao"), ("envio", "Envio"), ("aprovacao", "Aprovacao"), ("reprovacao", "Reprovacao"), ("cancelamento", "Cancelamento"), ("expiracao", "Expiracao"), ("conversao_os", "Conversao em OS"), ("pdf", "Geracao de PDF")], db_index=True, max_length=30)),
                ("descricao", models.TextField()),
                ("status_anterior", models.CharField(blank=True, max_length=30)),
                ("status_novo", models.CharField(blank=True, max_length=30)),
                ("dados_extras", models.JSONField(blank=True, default=dict)),
                ("orcamento", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="historico", to="orcamentos.orcamento")),
                ("usuario_responsavel", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="historicos_orcamento", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.AddConstraint(model_name="orcamento", constraint=models.CheckConstraint(check=models.Q(valor_produtos__gte=0), name="orc_valor_produtos_gte_0")),
        migrations.AddConstraint(model_name="orcamento", constraint=models.CheckConstraint(check=models.Q(valor_servicos__gte=0), name="orc_valor_servicos_gte_0")),
        migrations.AddConstraint(model_name="orcamento", constraint=models.CheckConstraint(check=models.Q(valor_desconto__gte=0), name="orc_valor_desconto_gte_0")),
        migrations.AddConstraint(model_name="orcamento", constraint=models.CheckConstraint(check=models.Q(valor_total__gte=0), name="orc_valor_total_gte_0")),
        migrations.AddConstraint(model_name="orcamento", constraint=models.CheckConstraint(check=models.Q(custo_total__gte=0), name="orc_custo_total_gte_0")),
        migrations.AddIndex(model_name="orcamento", index=models.Index(fields=["status", "data_criacao"], name="orcamentos_status_2f75d3_idx")),
        migrations.AddIndex(model_name="orcamento", index=models.Index(fields=["cliente", "status"], name="orcamentos_cliente_5554d1_idx")),
        migrations.AddIndex(model_name="orcamento", index=models.Index(fields=["data_validade"], name="orcamentos_data_va_328768_idx")),
        migrations.AddConstraint(model_name="itemprodutoorcamento", constraint=models.CheckConstraint(check=models.Q(quantidade__gt=0), name="orc_item_prod_quantidade_gt_0")),
        migrations.AddConstraint(model_name="itemprodutoorcamento", constraint=models.CheckConstraint(check=models.Q(valor_unitario__gte=0), name="orc_item_prod_valor_unit_gte_0")),
        migrations.AddConstraint(model_name="itemprodutoorcamento", constraint=models.CheckConstraint(check=models.Q(custo_unitario__gte=0), name="orc_item_prod_custo_unit_gte_0")),
        migrations.AddConstraint(model_name="itemprodutoorcamento", constraint=models.CheckConstraint(check=models.Q(desconto__gte=0), name="orc_item_prod_desconto_gte_0")),
        migrations.AddConstraint(model_name="itemservicoorcamento", constraint=models.CheckConstraint(check=models.Q(quantidade__gt=0), name="orc_item_serv_quantidade_gt_0")),
        migrations.AddConstraint(model_name="itemservicoorcamento", constraint=models.CheckConstraint(check=models.Q(valor_unitario__gte=0), name="orc_item_serv_valor_unit_gte_0")),
        migrations.AddConstraint(model_name="itemservicoorcamento", constraint=models.CheckConstraint(check=models.Q(custo_estimado__gte=0), name="orc_item_serv_custo_gte_0")),
        migrations.AddConstraint(model_name="itemservicoorcamento", constraint=models.CheckConstraint(check=models.Q(desconto__gte=0), name="orc_item_serv_desconto_gte_0")),
        migrations.AddIndex(model_name="historicoorcamento", index=models.Index(fields=["orcamento", "tipo_evento"], name="orcamentos_orcamen_d808ca_idx")),
    ]
