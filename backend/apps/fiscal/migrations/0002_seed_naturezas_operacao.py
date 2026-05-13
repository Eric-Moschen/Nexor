# Generated for Prompt 05 fiscal module seed data.

from django.db import migrations


def seed_naturezas(apps, schema_editor):
    NaturezaOperacao = apps.get_model("fiscal", "NaturezaOperacao")
    seeds = [
        {
            "codigo": "VENDA-5102",
            "descricao": "Venda de mercadoria adquirida de terceiros",
            "tipo_operacao": "venda",
            "cfop_padrao": "5102",
            "movimenta_estoque": True,
            "gera_financeiro": True,
        },
        {
            "codigo": "COMPRA-1102",
            "descricao": "Compra para comercializacao",
            "tipo_operacao": "compra",
            "cfop_padrao": "1102",
            "movimenta_estoque": True,
            "gera_financeiro": True,
        },
        {
            "codigo": "DEVOLUCAO-5202",
            "descricao": "Devolucao de compra para comercializacao",
            "tipo_operacao": "devolucao",
            "cfop_padrao": "5202",
            "movimenta_estoque": True,
            "gera_financeiro": False,
        },
    ]
    for seed in seeds:
        NaturezaOperacao.objects.get_or_create(codigo=seed["codigo"], defaults=seed)


class Migration(migrations.Migration):
    dependencies = [
        ("fiscal", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_naturezas, migrations.RunPython.noop),
    ]
