# Generated for Prompt 07 commercial budgets permissions.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_add_fiscal_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("administrador", "Administrador"),
                    ("comercial", "Comercial"),
                    ("fiscal", "Fiscal"),
                    ("financeiro", "Financeiro"),
                    ("estoque", "Estoque"),
                    ("compras", "Compras"),
                    ("operacional", "Operacional"),
                    ("supervisor", "Supervisor"),
                ],
                default="operacional",
                max_length=30,
            ),
        ),
    ]
