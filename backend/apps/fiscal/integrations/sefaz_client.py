from dataclasses import dataclass


@dataclass
class SefazResponse:
    autorizado: bool
    codigo: str
    mensagem: str
    protocolo: str = ""
    xml_retorno: str = ""


class SefazClient:
    def enviar_nfe(self, xml, ambiente):
        if ambiente == "homologacao":
            return SefazResponse(True, "100", "Autorizado o uso da NF-e", "HOMOLOG-0001", "<retorno>autorizado</retorno>")
        return SefazResponse(False, "999", "Integracao de producao nao configurada", "", "<retorno>pendente</retorno>")

    def cancelar_nfe(self, nota, justificativa):
        return SefazResponse(True, "135", "Evento de cancelamento registrado", f"CANC-{nota.id}", "<cancelamento>ok</cancelamento>")
