# Generated for the Prompt 03 purchasing module baseline.

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
            name="Fornecedor",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                ("razao_social", models.CharField(db_index=True, max_length=180)),
                ("nome_fantasia", models.CharField(blank=True, max_length=180)),
                ("documento", models.CharField(db_index=True, max_length=20, unique=True)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("telefone", models.CharField(blank=True, max_length=30)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="fornecedor_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="fornecedor_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["razao_social"]},
        ),
        migrations.AddIndex(model_name="fornecedor", index=models.Index(fields=["razao_social", "is_active"], name="fornecedor_razao_0cc95d_idx")),
        migrations.AddIndex(model_name="fornecedor", index=models.Index(fields=["documento", "is_active"], name="fornecedor_doc_85f6df_idx")),
    ]
