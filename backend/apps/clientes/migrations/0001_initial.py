# Generated for the Prompt 04 financial module baseline.

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
            name="Cliente",
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
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="cliente_created", to=settings.AUTH_USER_MODEL)),
                ("updated_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="cliente_updated", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["razao_social"]},
        ),
        migrations.AddIndex(model_name="cliente", index=models.Index(fields=["razao_social", "is_active"], name="cliente_razao_7c2f01_idx")),
        migrations.AddIndex(model_name="cliente", index=models.Index(fields=["documento", "is_active"], name="cliente_doc_cfdc63_idx")),
    ]
