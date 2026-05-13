from apps.ordens_servico.models import OrdensServicoRecord


def list_records():
    return OrdensServicoRecord.objects.filter(is_active=True).order_by("name")
