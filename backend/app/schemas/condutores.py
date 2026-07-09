from datetime import date, datetime

from pydantic import BaseModel, EmailStr


class UnidadeSimples(BaseModel):
    id: int
    nome: str
    sigla: str = ""
    model_config = {"from_attributes": True}


class SubunidadeSimples(BaseModel):
    id: int
    nome: str
    sigla: str = ""
    model_config = {"from_attributes": True}


class CondutorBase(BaseModel):
    prontuario: str
    status: str = "ATIVO"
    nome: str
    data_nascimento: date
    cpf: str
    rg: str = ""
    orgao_emissor: str = ""
    cargo: str = ""
    endereco: str = ""
    telefone: str = ""
    email: str = ""
    unidade_id: int | None = None
    subunidade_id: int | None = None
    cnh_categoria: str = ""
    cnh_numero: str = ""
    cnh_emissao: date | None = None
    cnh_vencimento: date | None = None
    cnh_orgao: str = ""


class CondutorCreate(CondutorBase):
    pass


class CondutorUpdate(BaseModel):
    status: str | None = None
    nome: str | None = None
    data_nascimento: date | None = None
    rg: str | None = None
    orgao_emissor: str | None = None
    cargo: str | None = None
    endereco: str | None = None
    telefone: str | None = None
    email: str | None = None
    unidade_id: int | None = None
    subunidade_id: int | None = None
    cnh_categoria: str | None = None
    cnh_numero: str | None = None
    cnh_emissao: date | None = None
    cnh_vencimento: date | None = None
    cnh_orgao: str | None = None


class CondutorResponse(CondutorBase):
    id: int
    foto: str | None = None
    cnh_arquivo: str | None = None
    unidade: UnidadeSimples | None = None
    subunidade: SubunidadeSimples | None = None

    model_config = {"from_attributes": True}


class CondutorListItem(BaseModel):
    id: int
    prontuario: str
    nome: str
    status: str
    unidade_id: int | None = None
    subunidade_id: int | None = None
    unidade: UnidadeSimples | None = None
    subunidade: SubunidadeSimples | None = None

    model_config = {"from_attributes": True}


class CondutorDocumentoResponse(BaseModel):
    id: int
    condutor_id: int
    tipo: str
    descricao: str
    arquivo: str
    criado_em: datetime

    model_config = {"from_attributes": True}
