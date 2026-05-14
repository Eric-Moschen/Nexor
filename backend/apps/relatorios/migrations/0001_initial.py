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
            name="RelatoriosRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("name", models.CharField(db_index=True, max_length=150)),
                ("description", models.TextField(blank=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="relatoriosrecord_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="relatoriosrecord_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="DashboardCache",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("chave", models.CharField(db_index=True, max_length=180, unique=True)),
                ("tipo_dashboard", models.CharField(choices=[("executivo", "Executivo"), ("financeiro", "Financeiro"), ("estoque", "Estoque"), ("comercial", "Comercial"), ("operacional", "Operacional")], db_index=True, max_length=30)),
                ("filtros", models.JSONField(blank=True, default=dict)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("expires_at", models.DateTimeField(db_index=True)),
                ("gerado_por", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="dashboards_cache", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-updated_at"]},
        ),
        migrations.CreateModel(
            name="RelatorioGerado",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("tipo_relatorio", models.CharField(choices=[("financeiro", "Financeiro"), ("estoque", "Estoque"), ("comercial", "Comercial"), ("os", "Ordens de servico"), ("compras", "Compras")], db_index=True, max_length=30)),
                ("titulo", models.CharField(max_length=180)),
                ("filtros", models.JSONField(blank=True, default=dict)),
                ("payload", models.JSONField(blank=True, default=dict)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="relatoriogerado_created", to=settings.AUTH_USER_MODEL)),
                ("gerado_por", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="relatorios_gerados", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="relatoriogerado_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.CreateModel(
            name="ExportacaoArquivo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("tipo_relatorio", models.CharField(choices=[("financeiro", "Financeiro"), ("estoque", "Estoque"), ("comercial", "Comercial"), ("os", "Ordens de servico"), ("compras", "Compras")], db_index=True, max_length=30)),
                ("formato", models.CharField(choices=[("pdf", "PDF"), ("excel", "Excel"), ("csv", "CSV")], db_index=True, max_length=10)),
                ("status", models.CharField(choices=[("pendente", "Pendente"), ("processando", "Processando"), ("concluida", "Concluida"), ("falhou", "Falhou")], db_index=True, default="pendente", max_length=20)),
                ("filtros", models.JSONField(blank=True, default=dict)),
                ("arquivo", models.FileField(blank=True, upload_to="relatorios/")),
                ("erro", models.TextField(blank=True)),
                ("task_id", models.CharField(blank=True, db_index=True, max_length=120)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="exportacaoarquivo_created", to=settings.AUTH_USER_MODEL)),
                ("relatorio", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="exportacoes", to="relatorios.relatoriogerado")),
                ("solicitado_por", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="exportacoes_relatorios", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="exportacaoarquivo_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-created_at", "-id"]},
        ),
        migrations.AddIndex(model_name="relatoriosrecord", index=models.Index(fields=["name", "is_active"], name="relatorios_name_4de7a4_idx")),
        migrations.AddIndex(model_name="dashboardcache", index=models.Index(fields=["tipo_dashboard", "expires_at"], name="rel_dash_tipo_9a60be_idx")),
        migrations.AddIndex(model_name="relatoriogerado", index=models.Index(fields=["tipo_relatorio", "created_at"], name="rel_ger_tipo_9ce657_idx")),
        migrations.AddIndex(model_name="relatoriogerado", index=models.Index(fields=["gerado_por", "created_at"], name="rel_ger_user_7d581b_idx")),
        migrations.AddIndex(model_name="exportacaoarquivo", index=models.Index(fields=["solicitado_por", "status"], name="rel_exp_user_status_824cb1_idx")),
        migrations.AddIndex(model_name="exportacaoarquivo", index=models.Index(fields=["tipo_relatorio", "formato"], name="rel_exp_tipo_form_1f86c2_idx")),
    ]
