from apps.ordens_servico.models import ApontamentoHorasOS, MaterialUtilizadoOS, OrdemServico


class OrdemServicoRepository:
    def get_for_update(self, ordem_id):
        return OrdemServico.objects.select_for_update().get(id=ordem_id, is_active=True)

    def get_active(self, ordem_id):
        return OrdemServico.objects.get(id=ordem_id, is_active=True)


class MaterialOSRepository:
    def get_for_update(self, material_id):
        return MaterialUtilizadoOS.objects.select_for_update().select_related("ordem_servico", "produto").get(id=material_id)


class ApontamentoOSRepository:
    def get_for_update(self, apontamento_id):
        return ApontamentoHorasOS.objects.select_for_update().select_related("ordem_servico").get(id=apontamento_id)
