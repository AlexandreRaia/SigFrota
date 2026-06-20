from datetime import datetime

from pydantic import BaseModel


class MensagemCreate(BaseModel):
    texto: str


class MensagemResponse(BaseModel):
    id: int
    smv_id: int
    etapa: str
    autor_id: int
    texto: str
    anexo: str | None = None
    enviada_em: datetime
    lida: bool = False

    model_config = {"from_attributes": True}


class MarcarLidaRequest(BaseModel):
    mensagem_ids: list[int]
