# Generated for the Prompt 02 stock module baseline.

import decimal
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CategoriaProduto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("nome", models.CharField(db_index=True, max_length=120, unique=True)),
                ("descricao", models.TextField(blank=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="categoriaproduto_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="categoriaproduto_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="UnidadeMedida",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("sigla", models.CharField(db_index=True, max_length=10, unique=True)),
                ("nome", models.CharField(max_length=80)),
                ("descricao", models.TextField(blank=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="unidademedida_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="unidademedida_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["sigla"]},
        ),
        migrations.CreateModel(
            name="Produto",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("codigo_interno", models.CharField(db_index=True, max_length=40, unique=True)),
                ("sku", models.CharField(db_index=True, max_length=60, unique=True)),
                ("codigo_barras", models.CharField(blank=True, db_index=True, max_length=80)),
                ("nome", models.CharField(db_index=True, max_length=180)),
                ("descricao", models.TextField(blank=True)),
                ("marca", models.CharField(blank=True, max_length=120)),
                ("custo_medio", models.DecimalField(decimal_places=4, default=decimal.Decimal("0.0000"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("preco_venda", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("estoque_minimo", models.DecimalField(decimal_places=4, default=decimal.Decimal("0.0000"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("estoque_atual", models.DecimalField(decimal_places=4, default=decimal.Decimal("0.0000"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))])),
                ("categoria", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="produtos", to="estoque.categoriaproduto")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="produto_created", to=settings.AUTH_USER_MODEL)),
                ("unidade_medida", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="produtos", to="estoque.unidademedida")),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="produto_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["nome"]},
        ),
        migrations.CreateModel(
            name="MovimentacaoEstoque",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("tipo", models.CharField(choices=[("entrada", "Entrada"), ("saida", "Saida"), ("ajuste", "Ajuste"), ("transferencia", "Transferencia")], db_index=True, max_length=20)),
                ("quantidade", models.DecimalField(decimal_places=4, max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0.0001"))])),
                ("saldo_anterior", models.DecimalField(decimal_places=4, max_digits=14)),
                ("saldo_posterior", models.DecimalField(decimal_places=4, max_digits=14)),
                ("observacao", models.TextField(blank=True)),
                ("data_movimentacao", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("produto", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="movimentacoes", to="estoque.produto")),
                ("usuario_responsavel", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="movimentacoes_estoque", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-data_movimentacao", "-id"]},
        ),
        migrations.AddIndex(model_name="categoriaproduto", index=models.Index(fields=["nome", "is_active"], name="estoque_cat_nome_84ff4b_idx")),
        migrations.AddIndex(model_name="unidademedida", index=models.Index(fields=["sigla", "is_active"], name="estoque_uni_sigla_4fc064_idx")),
        migrations.AddConstraint(model_name="produto", constraint=models.CheckConstraint(check=models.Q(estoque_minimo__gte=0), name="estoque_produto_minimo_gte_0")),
        migrations.AddConstraint(model_name="produto", constraint=models.CheckConstraint(check=models.Q(estoque_atual__gte=0), name="estoque_produto_atual_gte_0")),
        migrations.AddConstraint(model_name="produto", constraint=models.CheckConstraint(check=models.Q(custo_medio__gte=0), name="estoque_produto_custo_gte_0")),
        migrations.AddConstraint(model_name="produto", constraint=models.CheckConstraint(check=models.Q(preco_venda__gte=0), name="estoque_produto_preco_gte_0")),
        migrations.AddIndex(model_name="produto", index=models.Index(fields=["nome", "is_active"], name="estoque_pro_nome_554fe2_idx")),
        migrations.AddIndex(model_name="produto", index=models.Index(fields=["codigo_interno", "is_active"], name="estoque_pro_codigo_7658dd_idx")),
        migrations.AddIndex(model_name="produto", index=models.Index(fields=["sku", "is_active"], name="estoque_pro_sku_5c901d_idx")),
        migrations.AddIndex(model_name="produto", index=models.Index(fields=["categoria", "is_active"], name="estoque_pro_categor_782d8b_idx")),
        migrations.AddConstraint(model_name="movimentacaoestoque", constraint=models.CheckConstraint(check=models.Q(quantidade__gt=0), name="estoque_mov_quantidade_gt_0")),
        migrations.AddConstraint(model_name="movimentacaoestoque", constraint=models.CheckConstraint(check=models.Q(saldo_posterior__gte=0), name="estoque_mov_saldo_posterior_gte_0")),
        migrations.AddIndex(model_name="movimentacaoestoque", index=models.Index(fields=["produto", "tipo"], name="estoque_mov_produto_018275_idx")),
        migrations.AddIndex(model_name="movimentacaoestoque", index=models.Index(fields=["data_movimentacao"], name="estoque_mov_data_mo_3ff897_idx")),
    ]
