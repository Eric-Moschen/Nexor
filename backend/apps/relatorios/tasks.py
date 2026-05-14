from celery import shared_task

from apps.relatorios.services import RelatorioService


@shared_task(bind=True)
def gerar_exportacao_relatorio(self, exportacao_id):
    exportacao = RelatorioService().processar_exportacao(exportacao_id=exportacao_id)
    return {"exportacao_id": exportacao.id, "status": exportacao.status}
