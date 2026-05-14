import decimal
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clientes", "0001_initial"),
        ("fornecedores", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="cliente",
            name="documento",
            field=models.CharField(db_index=True, max_length=20),
        ),
        migrations.AddField(
            model_name="cliente",
            name="tipo_pessoa",
            field=models.CharField(choices=[("fisica", "Pessoa Fisica"), ("juridica", "Pessoa Juridica")], default="juridica", max_length=20),
        ),
        migrations.AddField(
            model_name="cliente",
            name="inscricao_estadual",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name="cliente",
            name="inscricao_municipal",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name="cliente",
            name="whatsapp",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name="cliente",
            name="status",
            field=models.CharField(choices=[("ativo", "Ativo"), ("inativo", "Inativo"), ("bloqueado", "Bloqueado")], db_index=True, default="ativo", max_length=20),
        ),
        migrations.AddField(
            model_name="cliente",
            name="limite_credito",
            field=models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=14, validators=[django.core.validators.MinValueValidator(decimal.Decimal("0"))]),
        ),
        migrations.AddField(
            model_name="cliente",
            name="observacoes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="cliente",
            name="usuario_responsavel",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="clientes_responsavel", to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name="EnderecoRelacionamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("cep", models.CharField(max_length=8)),
                ("rua", models.CharField(max_length=180)),
                ("numero", models.CharField(max_length=20)),
                ("complemento", models.CharField(blank=True, max_length=120)),
                ("bairro", models.CharField(max_length=120)),
                ("cidade", models.CharField(max_length=120)),
                ("uf", models.CharField(max_length=2)),
                ("codigo_ibge", models.CharField(blank=True, max_length=7)),
                ("tipo", models.CharField(choices=[("comercial", "Comercial"), ("cobranca", "Cobranca"), ("entrega", "Entrega"), ("fiscal", "Fiscal")], default="comercial", max_length=20)),
                ("cliente", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="enderecos", to="clientes.cliente")),
                ("fornecedor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="enderecos", to="fornecedores.fornecedor")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="enderecorelacionamento_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="enderecorelacionamento_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["tipo", "cidade"]},
        ),
        migrations.CreateModel(
            name="ContatoRelacionamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("nome", models.CharField(max_length=140)),
                ("cargo", models.CharField(blank=True, max_length=100)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("telefone", models.CharField(blank=True, max_length=30)),
                ("whatsapp", models.CharField(blank=True, max_length=30)),
                ("observacao", models.TextField(blank=True)),
                ("principal", models.BooleanField(default=False)),
                ("cliente", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="contatos", to="clientes.cliente")),
                ("fornecedor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="contatos", to="fornecedores.fornecedor")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="contatorelacionamento_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="contatorelacionamento_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-principal", "nome"]},
        ),
        migrations.CreateModel(
            name="HistoricoRelacionamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("tipo_evento", models.CharField(choices=[("criacao", "Criacao"), ("alteracao", "Alteracao"), ("bloqueio", "Bloqueio"), ("inativacao", "Inativacao"), ("interacao", "Interacao"), ("orcamento", "Orcamento"), ("ordem_servico", "Ordem de servico"), ("compra", "Compra"), ("nfe", "NFe"), ("documento", "Documento")], db_index=True, max_length=30)),
                ("descricao", models.TextField()),
                ("dados_extras", models.JSONField(blank=True, default=dict)),
                ("cliente", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="historico_relacionamento", to="clientes.cliente")),
                ("fornecedor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="historico_relacionamento", to="fornecedores.fornecedor")),
                ("usuario_responsavel", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="historicos_relacionamento", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.CreateModel(
            name="InteracaoCRM",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("tipo_interacao", models.CharField(choices=[("ligacao", "Ligacao"), ("whatsapp", "WhatsApp"), ("email", "Email"), ("visita", "Visita"), ("reuniao", "Reuniao"), ("suporte", "Suporte"), ("pos_venda", "Pos-venda")], db_index=True, max_length=20)),
                ("descricao", models.TextField()),
                ("data", models.DateTimeField(db_index=True)),
                ("proximo_contato", models.DateTimeField(blank=True, null=True)),
                ("status", models.CharField(choices=[("aberto", "Aberto"), ("em_andamento", "Em andamento"), ("finalizado", "Finalizado")], db_index=True, default="aberto", max_length=20)),
                ("cliente", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="interacoes", to="clientes.cliente")),
                ("responsavel", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="interacoes_crm", to=settings.AUTH_USER_MODEL)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="interacaocrm_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="interacaocrm_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-data", "-id"]},
        ),
        migrations.CreateModel(
            name="DocumentoRelacionamento",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("tipo_documento", models.CharField(max_length=80)),
                ("titulo", models.CharField(max_length=160)),
                ("arquivo", models.FileField(upload_to="relacionamentos/")),
                ("observacao", models.TextField(blank=True)),
                ("cliente", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="documentos", to="clientes.cliente")),
                ("fornecedor", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="documentos", to="fornecedores.fornecedor")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="documentorelacionamento_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="documentorelacionamento_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.AddConstraint(
            model_name="cliente",
            constraint=models.UniqueConstraint(condition=models.Q(is_active=True), fields=("documento",), name="clientes_documento_ativo_uniq"),
        ),
        migrations.AddConstraint(
            model_name="cliente",
            constraint=models.CheckConstraint(check=models.Q(limite_credito__gte=0), name="clientes_limite_credito_gte_0"),
        ),
        migrations.AddIndex(
            model_name="cliente",
            index=models.Index(fields=["status", "is_active"], name="clientes_status_dba807_idx"),
        ),
        migrations.AddConstraint(
            model_name="enderecorelacionamento",
            constraint=models.CheckConstraint(check=models.Q(cliente__isnull=False, fornecedor__isnull=True) | models.Q(cliente__isnull=True, fornecedor__isnull=False), name="rel_endereco_cliente_ou_fornecedor"),
        ),
        migrations.AddConstraint(
            model_name="contatorelacionamento",
            constraint=models.CheckConstraint(check=models.Q(cliente__isnull=False, fornecedor__isnull=True) | models.Q(cliente__isnull=True, fornecedor__isnull=False), name="rel_contato_cliente_ou_fornecedor"),
        ),
        migrations.AddConstraint(
            model_name="historicorelacionamento",
            constraint=models.CheckConstraint(check=models.Q(cliente__isnull=False, fornecedor__isnull=True) | models.Q(cliente__isnull=True, fornecedor__isnull=False), name="rel_historico_cliente_ou_fornecedor"),
        ),
        migrations.AddConstraint(
            model_name="documentorelacionamento",
            constraint=models.CheckConstraint(check=models.Q(cliente__isnull=False, fornecedor__isnull=True) | models.Q(cliente__isnull=True, fornecedor__isnull=False), name="rel_documento_cliente_ou_fornecedor"),
        ),
        migrations.AddIndex(model_name="enderecorelacionamento", index=models.Index(fields=["cliente", "tipo"], name="rel_end_cli_tipo_e63ee6_idx")),
        migrations.AddIndex(model_name="enderecorelacionamento", index=models.Index(fields=["fornecedor", "tipo"], name="rel_end_for_tipo_87bdc5_idx")),
        migrations.AddIndex(model_name="enderecorelacionamento", index=models.Index(fields=["cep"], name="rel_end_cep_01f033_idx")),
        migrations.AddIndex(model_name="contatorelacionamento", index=models.Index(fields=["cliente", "principal"], name="rel_cont_cli_princ_17db10_idx")),
        migrations.AddIndex(model_name="contatorelacionamento", index=models.Index(fields=["fornecedor", "principal"], name="rel_cont_for_princ_5cc4fd_idx")),
        migrations.AddIndex(model_name="contatorelacionamento", index=models.Index(fields=["email"], name="rel_cont_email_65f465_idx")),
        migrations.AddIndex(model_name="historicorelacionamento", index=models.Index(fields=["cliente", "tipo_evento"], name="rel_hist_cli_tipo_31cf7d_idx")),
        migrations.AddIndex(model_name="historicorelacionamento", index=models.Index(fields=["fornecedor", "tipo_evento"], name="rel_hist_for_tipo_f0b607_idx")),
        migrations.AddIndex(model_name="interacaocrm", index=models.Index(fields=["cliente", "status"], name="crm_inter_cli_status_521fc1_idx")),
        migrations.AddIndex(model_name="interacaocrm", index=models.Index(fields=["responsavel", "data"], name="crm_inter_resp_data_5d9973_idx")),
    ]
