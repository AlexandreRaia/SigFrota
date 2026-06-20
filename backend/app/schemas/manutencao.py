from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


class SMVCreate(BaseModel):
    veiculo_id: int
    descricao_problema: str
    urgencia: str = "MEDIA"
    km_entrada: int | None = None
    observacoes: str = ""


class SMVUpdate(BaseModel):
    urgencia: str | None = None
    descricao_problema: str | None = None
    km_entrada: int | None = None
    km_saida: int | None = None
    diagnostico: str | None = None
    tipos_servico: str | None = None
    observacoes: str | None = None


class SMVAvancarEtapa(BaseModel):
    etapa_para: str
    observacao: str = ""


class SMVOrcamentoCreate(BaseModel):
    fornecedor: str
    valor_mao_obra: Decimal
    valor_pecas: Decimal
    observacao: str = ""


class SMVDiagnosticoItemCreate(BaseModel):
    tipo: str = "PECA"
    descricao: str
    quantidade: Decimal = Decimal("1")
    valor_unitario: Decimal | None = None


class SMVMensagemCreate(BaseModel):
    texto: str


# ── Responses ──────────────────────────────────────────────────────────────────

class SMVEtapaResponse(BaseModel):
    id: int
    etapa_de: str
    etapa_para: str
    observacao: str
    data: datetime
    responsavel_id: int

    model_config = {"from_attributes": True}


class SMVOrcamentoResponse(BaseModel):
    id: int
    fornecedor: str
    valor_mao_obra: Decimal
    valor_pecas: Decimal
    valor_total: Decimal
    aprovado: bool | None = None
    observacao: str

    model_config = {"from_attributes": True}


class SMVDiagnosticoItemResponse(BaseModel):
    id: int
    tipo: str
    descricao: str
    quantidade: Decimal
    valor_unitario: Decimal | None = None

    model_config = {"from_attributes": True}


class SMVResponse(BaseModel):
    id: int
    numero: str
    veiculo_id: int
    solicitante_id: int
    etapa: str
    urgencia: str
    descricao_problema: str
    km_entrada: int | None = None
    km_saida: int | None = None
    diagnostico: str
    observacoes: str
    dt_solicitacao: datetime
    dt_recepcao: datetime | None = None
    dt_diagnostico: datetime | None = None
    dt_inicio_exec: datetime | None = None
    dt_retirada: datetime | None = None
    dt_finalizacao: datetime | None = None

    model_config = {"from_attributes": True}


class SMVDetalheResponse(SMVResponse):
    historico_etapas: list[SMVEtapaResponse] = []
    orcamentos: list[SMVOrcamentoResponse] = []
    itens_diagnostico: list[SMVDiagnosticoItemResponse] = []


class SMVListItem(BaseModel):
    id: int
    numero: str
    veiculo_id: int
    etapa: str
    urgencia: str
    dt_solicitacao: datetime
    msgs_nao_lidas: int = 0

    model_config = {"from_attributes": True}
