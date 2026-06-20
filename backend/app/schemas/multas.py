from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TipoMultaResponse(BaseModel):
    id: int
    codigo: str
    descricao: str
    natureza: str
    ativo: bool

    model_config = {"from_attributes": True}


class MultaBase(BaseModel):
    placa: str
    condutor_id: int | None = None
    tipo_infracao_id: int | None = None
    pontos: int = 0
    valor: Decimal
    data_infracao: date
    status: str = "PENDENTE"
    data_vencimento: date
    prazo_indicacao: date | None = None
    prazo_defesa: date | None = None
    observacao: str = ""


class MultaCreate(MultaBase):
    pass


class MultaUpdate(BaseModel):
    condutor_id: int | None = None
    status: str | None = None
    prazo_indicacao: date | None = None
    prazo_defesa: date | None = None
    observacao: str | None = None


class MultaResponse(MultaBase):
    id: int
    arquivo: str | None = None
    tipo_infracao: TipoMultaResponse | None = None

    model_config = {"from_attributes": True}


class MultaListItem(BaseModel):
    id: int
    placa: str
    data_infracao: date
    valor: Decimal
    status: str
    pontos: int
    data_vencimento: date

    model_config = {"from_attributes": True}
