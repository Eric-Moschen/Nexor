import json

from django.core.files.base import ContentFile


class PDFExporter:
    extension = "pdf"

    def export(self, relatorio):
        body = json.dumps(relatorio.payload, ensure_ascii=False, indent=2, default=str)
        # Minimal PDF-like artifact; the exporter boundary keeps room for a full renderer later.
        content = f"%PDF-1.4\n% Nexor ERP\n1 0 obj <<>> endobj\n2 0 obj << /Length {len(body)} >> stream\n{body}\nendstream endobj\n%%EOF"
        filename = f"relatorio-{relatorio.tipo_relatorio}-{relatorio.id}.pdf"
        return filename, ContentFile(content.encode("utf-8"))
