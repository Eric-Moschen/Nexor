from apps.ordens_servico.models import OrdensServicoRecord


def create_record(*, name, description="", created_by=None):
    return OrdensServicoRecord.objects.create(name=name, description=description, created_by=created_by)
