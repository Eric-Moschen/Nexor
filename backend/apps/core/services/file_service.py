from pathlib import Path

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


class FileService:
    def save_generated_file(self, *, path, content, content_type="application/octet-stream"):
        normalized = str(Path(path))
        file_obj = ContentFile(content.encode("utf-8") if isinstance(content, str) else content)
        saved_path = default_storage.save(normalized, file_obj)
        return {"path": saved_path, "url": default_storage.url(saved_path), "content_type": content_type}

    def prepare_pdf_storage(self, *, folder, filename, content):
        return self.save_generated_file(path=f"{folder}/{filename}", content=content, content_type="application/pdf")

    def prepare_xml_storage(self, *, folder, filename, content):
        return self.save_generated_file(path=f"{folder}/{filename}", content=content, content_type="application/xml")
