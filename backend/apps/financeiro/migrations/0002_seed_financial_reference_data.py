from django.db import migrations


def seed_financial_data(apps, schema_editor):
    CentroCusto = apps.get_model("financeiro", "CentroCusto")
    CategoriaFinanceira = apps.get_model("financeiro", "CategoriaFinanceira")

    centros = [
        ("PROD", "Producao"),
        ("ADM", "Administrativo"),
        ("COMP", "Compras"),
        ("MAN", "Manutencao"),
        ("OPER", "Operacional"),
    ]
    categorias = [
        ("Vendas", "receita"),
        ("Servicos", "receita"),
        ("Materia prima", "despesa"),
        ("Manutencao", "despesa"),
        ("Administrativo", "despesa"),
    ]

    for codigo, nome in centros:
        CentroCusto.objects.get_or_create(codigo=codigo, defaults={"nome": nome})

    for nome, tipo in categorias:
        CategoriaFinanceira.objects.get_or_create(nome=nome, tipo=tipo)


class Migration(migrations.Migration):
    dependencies = [
        ("financeiro", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_financial_data, migrations.RunPython.noop),
    ]
