from dataclasses import dataclass, field


ORCAMENTO_APROVADO = "orcamento_aprovado"
OS_FINALIZADA = "os_finalizada"
OS_FATURADA = "os_faturada"
NFE_AUTORIZADA = "nfe_autorizada"
NFE_REJEITADA = "nfe_rejeitada"
PEDIDO_RECEBIDO = "pedido_recebido"
CONTA_PAGA = "conta_paga"
CONTA_RECEBIDA = "conta_recebida"
ESTOQUE_BAIXO = "estoque_baixo"
CLIENTE_BLOQUEADO = "cliente_bloqueado"
MATERIAL_OS_UTILIZADO = "material_os_utilizado"


@dataclass(frozen=True)
class InternalEvent:
    name: str
    module: str
    aggregate_type: str
    aggregate_id: str = ""
    payload: dict = field(default_factory=dict)
    user: object = None
    ip_address: str | None = None
