from django.core.files.base import ContentFile


class OrcamentoPdfGenerator:
    def generate(self, orcamento):
        lines = [
            f"ORCAMENTO {orcamento.numero}",
            f"Cliente: {orcamento.cliente.razao_social}",
            f"Titulo: {orcamento.titulo}",
            f"Validade: {orcamento.data_validade}",
            f"Total: {orcamento.valor_total}",
        ]
        content = "\n".join(lines).encode("utf-8")
        return ContentFile(content, name=f"orcamento-{orcamento.numero}.pdf")
