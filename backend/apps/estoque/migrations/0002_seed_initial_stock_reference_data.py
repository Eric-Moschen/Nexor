from django.db import migrations


def seed_reference_data(apps, schema_editor):
    CategoriaProduto = apps.get_model("estoque", "CategoriaProduto")
    UnidadeMedida = apps.get_model("estoque", "UnidadeMedida")

    categorias = [
        ("Materia prima", "Materiais utilizados na producao ou prestacao de servico."),
        ("Produto acabado", "Itens finalizados e prontos para venda ou entrega."),
        ("Insumos", "Itens de consumo operacional."),
    ]
    unidades = [
        ("UN", "Unidade"),
        ("KG", "Quilograma"),
        ("MT", "Metro"),
        ("CX", "Caixa"),
        ("PC", "Peca"),
    ]

    for nome, descricao in categorias:
        CategoriaProduto.objects.get_or_create(nome=nome, defaults={"descricao": descricao})

    for sigla, nome in unidades:
        UnidadeMedida.objects.get_or_create(sigla=sigla, defaults={"nome": nome})


class Migration(migrations.Migration):
    dependencies = [
        ("estoque", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_reference_data, migrations.RunPython.noop),
    ]
