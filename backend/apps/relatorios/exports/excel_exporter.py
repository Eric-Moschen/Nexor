from django.core.files.base import ContentFile

from apps.relatorios.exports.csv_exporter import CSVExporter


class ExcelExporter:
    extension = "xls"

    def export(self, relatorio):
        _, csv_content = CSVExporter().export(relatorio)
        filename = f"relatorio-{relatorio.tipo_relatorio}-{relatorio.id}.xls"
        html = (
            "<html><body><pre>"
            + csv_content.read().decode("utf-8").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            + "</pre></body></html>"
        )
        return filename, ContentFile(html.encode("utf-8"))
