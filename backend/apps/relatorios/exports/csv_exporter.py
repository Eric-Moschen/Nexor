import csv
import io
import json

from django.core.files.base import ContentFile


class CSVExporter:
    extension = "csv"

    def export(self, relatorio):
        buffer = io.StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["secao", "chave", "valor"])
        self._write_payload(writer, relatorio.payload)
        filename = f"relatorio-{relatorio.tipo_relatorio}-{relatorio.id}.csv"
        return filename, ContentFile(buffer.getvalue().encode("utf-8"))

    def _write_payload(self, writer, payload, prefix=""):
        if isinstance(payload, dict):
            for key, value in payload.items():
                self._write_payload(writer, value, f"{prefix}.{key}" if prefix else key)
            return
        if isinstance(payload, list):
            for index, value in enumerate(payload):
                self._write_payload(writer, value, f"{prefix}[{index}]")
            return
        writer.writerow([prefix.split(".")[0], prefix, json.dumps(payload, ensure_ascii=False, default=str)])
