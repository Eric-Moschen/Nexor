from celery import shared_task
from django.contrib.auth import get_user_model

from apps.fiscal.services import FiscalService


@shared_task
def enviar_nfe_task(nota_id, usuario_id):
    usuario = get_user_model().objects.get(id=usuario_id)
    nota = FiscalService().enviar_nfe(nota_id=nota_id, usuario=usuario)
    return nota.id


@shared_task
def gerar_danfe_task(nota_id):
    arquivo = FiscalService().gerar_danfe(nota_id=nota_id)
    return arquivo.name
