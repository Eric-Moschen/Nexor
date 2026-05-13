# Generated for Prompt 05 fiscal module permissions.

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("administrador", "Administrador"),
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
