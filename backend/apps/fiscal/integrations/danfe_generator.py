from django.core.files.base import ContentFile


class DanfeGenerator:
    def generate(self, nota):
        content = f"DANFE NFe {nota.numero}/{nota.serie} - {nota.valor_total}".encode("utf-8")
        return ContentFile(content, name=f"danfe-{nota.numero}-{nota.serie}.pdf")
