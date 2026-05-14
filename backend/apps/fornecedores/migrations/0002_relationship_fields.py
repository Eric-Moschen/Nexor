import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("fornecedores", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="fornecedor",
            name="documento",
            field=models.CharField(db_index=True, max_length=20),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="tipo_pessoa",
            field=models.CharField(choices=[("fisica", "Pessoa Fisica"), ("juridica", "Pessoa Juridica")], default="juridica", max_length=20),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="inscricao_estadual",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="whatsapp",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="categoria",
            field=models.CharField(choices=[("materia_prima", "Materia-prima"), ("ferramentas", "Ferramentas"), ("servicos", "Servicos"), ("transporte", "Transporte"), ("terceirizados", "Terceirizados"), ("outros", "Outros")], db_index=True, default="outros", max_length=30),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="status",
            field=models.CharField(choices=[("ativo", "Ativo"), ("inativo", "Inativo"), ("bloqueado", "Bloqueado")], db_index=True, default="ativo", max_length=20),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="observacoes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="fornecedor",
            name="usuario_responsavel",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="fornecedores_responsavel", to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name="fornecedor",
            constraint=models.UniqueConstraint(condition=models.Q(is_active=True), fields=("documento",), name="fornecedores_documento_ativo_uniq"),
        ),
        migrations.AddIndex(
            model_name="fornecedor",
            index=models.Index(fields=["status", "is_active"], name="fornec_status_44d094_idx"),
        ),
        migrations.AddIndex(
            model_name="fornecedor",
            index=models.Index(fields=["categoria", "is_active"], name="fornec_categoria_f798f3_idx"),
        ),
    ]
