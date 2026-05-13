# Generated for the Prompt 03 purchasing module baseline.

import decimal
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("estoque", "0001_initial"),
        ("fornecedores", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="SolicitacaoCompra",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("numero", models.CharField(db_index=True, max_length=30, unique=True)),
                ("centro_custo", models.CharField(max_length=120)),
                ("justificativa", models.TextField()),
                ("prioridade", models.CharField(choices=[("baixa", "Baixa"), ("media", "Media"), ("alta", "Alta"), ("urgente", "Urgente")], default="media", max_length=20)),
                ("status", models.CharField(choices=[("rascunho", "Rascunho"), ("pendente_aprovacao", "Pendente de aprovacao"), ("aprovada", "Aprovada"), ("reprovada", "Reprovada"), ("convertida_pedido", "Convertida em pedido"), ("cancelada", "Cancelada")], db_index=True, default="rascunho", max_length=30)),
                ("data_solicitacao", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("data_aprovacao", models.DateTimeField(blank=True, null=True)),
                ("observacoes", models.TextField(blank=True)),
                ("aprovador", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="aprovacoes_compra", to=settings.AUTH_USER_MODEL)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="solicitacaocompra_created", to=settings.AUTH_USER_MODEL)),
                ("solicitante", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="solicitacoes_compra", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="solicitacaocompra_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-data_solicitacao", "-id"]},
        ),
        migrations.CreateModel(
            name="PedidoCompra",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("numero", models.CharField(db_index=True, max_length=30, unique=True)),
                ("data_pedido", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("previsao_entrega", models.DateField(blank=True, null=True)),
                ("status", models.CharField(choices=[("aberto", "Aberto"), ("enviado_fornecedor", "Enviado ao fornecedor"), ("parcialmente_recebido", "Parcialmente recebido"), ("recebido", "Recebido"), ("cancelado", "Cancelado")], db_index=True, default="aberto", max_length=30)),
                ("valor_total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("observacoes", models.TextField(blank=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="pedidocompra_created", to=settings.AUTH_USER_MODEL)),
                ("fornecedor", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="pedidos_compra", to="fornecedores.fornecedor")),
                ("solicitacao_origem", models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="pedido", to="compras.solicitacaocompra")),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="pedidocompra_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-data_pedido", "-id"]},
        ),
        migrations.CreateModel(
            name="HistoricoAprovacaoCompra",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("acao", models.CharField(choices=[("enviar_aprovacao", "Enviar para aprovacao"), ("aprovar", "Aprovar"), ("reprovar", "Reprovar"), ("cancelar", "Cancelar"), ("converter_pedido", "Converter em pedido")], max_length=30)),
                ("status_anterior", models.CharField(blank=True, max_length=30)),
                ("status_posterior", models.CharField(max_length=30)),
                ("motivo", models.TextField(blank=True)),
                ("solicitacao", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="historico_aprovacao", to="compras.solicitacaocompra")),
                ("usuario", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.CreateModel(
            name="ItemSolicitacaoCompra",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("descricao_livre", models.CharField(blank=True, max_length=220)),
                ("quantidade_solicitada", models.DecimalField(decimal_places=4, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.0001"))])),
                ("observacao", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("aberto", "Aberto"), ("aprovado", "Aprovado"), ("reprovado", "Reprovado"), ("convertido", "Convertido")], db_index=True, default="aberto", max_length=20)),
                ("produto", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="itens_solicitacao_compra", to="estoque.produto")),
                ("solicitacao", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="itens", to="compras.solicitacaocompra")),
                ("unidade_medida", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="itens_solicitacao_compra", to="estoque.unidademedida")),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.CreateModel(
            name="ItemPedidoCompra",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("descricao", models.CharField(max_length=220)),
                ("quantidade", models.DecimalField(decimal_places=4, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.0001"))])),
                ("valor_unitario", models.DecimalField(decimal_places=2, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("valor_total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("quantidade_recebida", models.DecimalField(decimal_places=4, default=decimal.Decimal("0.0000"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("pedido", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="itens", to="compras.pedidocompra")),
                ("produto", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="itens_pedido_compra", to="estoque.produto")),
                ("unidade_medida", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="itens_pedido_compra", to="estoque.unidademedida")),
            ],
            options={"ordering": ["id"]},
        ),
        migrations.AddIndex(model_name="solicitacaocompra", index=models.Index(fields=["numero", "status"], name="compras_sol_numero_b0d6cf_idx")),
        migrations.AddIndex(model_name="solicitacaocompra", index=models.Index(fields=["solicitante", "status"], name="compras_sol_solicit_8f857d_idx")),
        migrations.AddIndex(model_name="solicitacaocompra", index=models.Index(fields=["data_solicitacao"], name="compras_sol_data_so_7a8392_idx")),
        migrations.AddIndex(model_name="pedidocompra", index=models.Index(fields=["numero", "status"], name="compras_ped_numero_a2e64a_idx")),
        migrations.AddIndex(model_name="pedidocompra", index=models.Index(fields=["fornecedor", "status"], name="compras_ped_fornece_471f99_idx")),
        migrations.AddIndex(model_name="pedidocompra", index=models.Index(fields=["data_pedido"], name="compras_ped_data_pe_01821b_idx")),
        migrations.AddIndex(model_name="historicoaprovacaocompra", index=models.Index(fields=["solicitacao", "acao"], name="compras_his_solicit_8694a5_idx")),
        migrations.AddIndex(model_name="historicoaprovacaocompra", index=models.Index(fields=["created_at"], name="compras_his_created_2ca268_idx")),
        migrations.AddConstraint(model_name="itemsolicitacaocompra", constraint=models.CheckConstraint(check=models.Q(quantidade_solicitada__gt=0), name="compras_item_solic_qtd_gt_0")),
        migrations.AddIndex(model_name="itemsolicitacaocompra", index=models.Index(fields=["solicitacao", "status"], name="compras_ite_solicit_8e7ef3_idx")),
        migrations.AddIndex(model_name="itemsolicitacaocompra", index=models.Index(fields=["produto"], name="compras_ite_produto_27ef13_idx")),
        migrations.AddConstraint(model_name="itempedidocompra", constraint=models.CheckConstraint(check=models.Q(quantidade__gt=0), name="compras_item_pedido_qtd_gt_0")),
        migrations.AddConstraint(model_name="itempedidocompra", constraint=models.CheckConstraint(check=models.Q(valor_unitario__gte=0), name="compras_item_pedido_vu_gte_0")),
        migrations.AddConstraint(model_name="itempedidocompra", constraint=models.CheckConstraint(check=models.Q(quantidade_recebida__gte=0), name="compras_item_pedido_qtd_rec_gte_0")),
        migrations.AddIndex(model_name="itempedidocompra", index=models.Index(fields=["pedido"], name="compras_ite_pedido_e1a2e3_idx")),
        migrations.AddIndex(model_name="itempedidocompra", index=models.Index(fields=["produto"], name="compras_ite_produto_2a58df_idx")),
    ]
