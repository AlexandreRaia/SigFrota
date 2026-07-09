from datetime import date, datetime
from pydantic import BaseModel, Field


# ── Entidades Parametrizadoras ──────────────────────────────────────────────

class CategoriaResponse(BaseModel):
    """Categoria de veículo (Passeio, Utilitário, Ambulância, etc)."""
    id: int
    nome: str
    descricao: str = ""
    ativa: bool

    model_config = {"from_attributes": True}


class CategoriaCreate(BaseModel):
    """Dados para criar uma categoria."""
    nome: str = Field(min_length=1, max_length=60)
    descricao: str = Field(default="", max_length=250)


class CategoriaUpdate(BaseModel):
    """Dados para atualizar uma categoria (campos opcionais)."""
    nome: str | None = Field(default=None, min_length=1, max_length=60)
    descricao: str | None = Field(default=None, max_length=250)
    ativa: bool | None = None


class TipoFrotaResponse(BaseModel):
    """Tipo de frota (Próprio, Alugado, Convênio)."""
    id: int
    nome: str
    ativa: bool

    model_config = {"from_attributes": True}


class TipoFrotaCreate(BaseModel):
    """Dados para criar um tipo de frota."""
    nome: str = Field(min_length=1, max_length=50)


class TipoFrotaUpdate(BaseModel):
    """Dados para atualizar um tipo de frota (campos opcionais)."""
    nome: str | None = Field(default=None, min_length=1, max_length=50)
    ativa: bool | None = None


class CombustivelResponse(BaseModel):
    """Tipo de combustível (GASOLINA, DIESEL, FLEX, etc.)."""
    id: int
    nome: str
    ativo: bool

    model_config = {"from_attributes": True}


class CombustivelCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=30)


class CombustivelUpdate(BaseModel):
    nome: str | None = Field(default=None, min_length=1, max_length=30)
    ativo: bool | None = None


class UnidadeResponse(BaseModel):
    """Unidade administrativa."""
    id: int
    nome: str
    sigla: str = ""
    secretaria_id: int | None = None
    ativa: bool

    model_config = {"from_attributes": True}


class UnidadeCreate(BaseModel):
    """Dados para criar uma unidade (equivale a uma Secretaria)."""
    nome: str = Field(min_length=1, max_length=120)
    sigla: str = Field(default="", max_length=20)
    secretaria_id: int | None = None


class UnidadeUpdate(BaseModel):
    """Dados para atualizar uma unidade (campos opcionais)."""
    nome: str | None = Field(default=None, min_length=1, max_length=120)
    secretaria_id: int | None = None
    sigla: str | None = Field(default=None, max_length=20)
    ativa: bool | None = None


class SubunidadeResponse(BaseModel):
    """Subunidade administrativa."""
    id: int
    nome: str
    sigla: str = ""
    unidade_id: int | None = None
    ativa: bool

    model_config = {"from_attributes": True}


class SubunidadeCreate(BaseModel):
    """Dados para criar uma subunidade."""
    nome: str = Field(min_length=1, max_length=120)
    unidade_id: int
    sigla: str = Field(default="", max_length=20)


class SubunidadeUpdate(BaseModel):
    """Dados para atualizar uma subunidade (campos opcionais)."""
    nome: str | None = Field(default=None, min_length=1, max_length=120)
    unidade_id: int | None = None
    sigla: str | None = Field(default=None, max_length=20)
    ativa: bool | None = None


class CentroCustoResponse(BaseModel):
    """Centro de custo para alocação de despesas."""
    id: int
    codigo: str
    nome: str
    ativa: bool

    model_config = {"from_attributes": True}


class CentroCustoCreate(BaseModel):
    """Dados para criar um centro de custo."""
    codigo: str = Field(min_length=1, max_length=20)
    nome: str = Field(min_length=1, max_length=120)


class CentroCustoUpdate(BaseModel):
    """Dados para atualizar um centro de custo (campos opcionais)."""
    codigo: str | None = Field(default=None, min_length=1, max_length=20)
    nome: str | None = Field(default=None, min_length=1, max_length=120)
    ativa: bool | None = None


# ── Marca e Modelo ──────────────────────────────────────────────────────────

class TipoVeiculoResponse(BaseModel):
    """Tipo de registro (VEICULO, MAQUINA, EQUIPAMENTO)."""
    id: int
    nome: str
    ativo: bool

    model_config = {"from_attributes": True}


class TipoVeiculoCreate(BaseModel):
    """Dados para criar um tipo de veículo."""
    nome: str = Field(min_length=1, max_length=50)


class TipoVeiculoUpdate(BaseModel):
    """Dados para atualizar um tipo de veículo (campos opcionais)."""
    nome: str | None = Field(default=None, min_length=1, max_length=50)
    ativo: bool | None = None


class MarcaResponse(BaseModel):
    id: int
    nome: str
    ativo: bool

    model_config = {"from_attributes": True}


class MarcaCreate(BaseModel):
    """Dados para criar uma marca."""
    nome: str = Field(min_length=1, max_length=60)


class MarcaUpdate(BaseModel):
    """Dados para atualizar uma marca (campos opcionais)."""
    nome: str | None = Field(default=None, min_length=1, max_length=60)
    ativo: bool | None = None


class ModeloResponse(BaseModel):
    id: int
    nome: str
    marca_id: int
    ativo: bool

    model_config = {"from_attributes": True}


class ModeloCreate(BaseModel):
    """Dados para criar um modelo."""
    nome: str = Field(min_length=1, max_length=100)
    marca_id: int


class ModeloUpdate(BaseModel):
    """Dados para atualizar um modelo (campos opcionais)."""
    nome: str | None = Field(default=None, min_length=1, max_length=100)
    marca_id: int | None = None
    ativo: bool | None = None


# ── Veículo ────────────────────────────────────────────────────────────────────

class VeiculoBase(BaseModel):
    """Base com todos os campos do veículo (8 seções conforme especificação)."""
    
    # 4.2.1 DADOS GERAIS
    placa: str = Field(..., description="Placa do veículo (ex: ABC-1234)")
    chassi: str = Field(..., description="Número do chassi")
    renavam: str = Field(..., description="RENAVAM do veículo")
    marca_id: int | None = None
    modelo_id: int | None = None
    ano_fabricacao: int = Field(..., description="Ano de fabricação")
    ano_modelo: int | None = None
    cor: str = ""
    combustivel: str = Field(default="FLEX", description="Tipo de combustível")
    motorizacao: str = ""
    observacoes: str = ""
    situacao: str = "ATIVA"
    
    # 4.2.2 CLASSIFICAÇÃO
    prefixo: str = Field(..., description="Prefixo identificador único")
    tipo_frota_id: int | None = None
    categoria_id: int | None = None
    numero_patrimonio: str | None = None
    valor_aquisicao: float | None = None
    tipo_aquisicao: str | None = None  # COMPRADO ou DOADO
    tipo_convenio: str | None = None  # PM ou BOMBEIROS
    nome_locador: str | None = None
    valor_locacao: float | None = None
    
    # 4.2.3 ADMINISTRATIVA
    secretaria_id: int | None = None
    unidade_id: int | None = None
    subunidade_id: int | None = None
    centro_custo_id: int | None = None
    
    # 4.2.4 OPERACIONAL
    tipo_registro_id: int | None = None
    tipo_controle: str = "QUILOMETRAGEM"  # QUILOMETRAGEM ou HORIMETRO
    hodometro_horimetro_inicial: int = 0
    capacidade_tanque: int | None = None
    capacidade_passageiros: int | None = None
    capacidade_carga: int | None = None
    
    # 4.2.5 DOCUMENTAÇÃO
    vencimento_licenciamento: date | None = None
    vencimento_seguro: date | None = None
    vencimento_ipva: date | None = None
    
    # 4.2.6 DADOS TÉCNICOS
    cilindrada: int | None = None
    potencia: int | None = None
    transmissao: str | None = None
    tracao: str | None = None
    vidros_eletricos: bool = False
    direcao: str | None = None
    ar_condicionado: bool = False
    pneu_dimensao: str | None = None
    pneu_velocidade: str | None = None
    pneu_carga: str | None = None
    
    # 4.2.7 LOCALIZAÇÃO
    uf: str = "SP"
    municipio: str = ""


class VeiculoCreate(VeiculoBase):
    """Schema para criar um veículo."""
    pass


class VeiculoUpdate(BaseModel):
    """Schema para atualizar um veículo (todos os campos opcionais)."""
    
    # 4.2.1 DADOS GERAIS
    placa: str | None = None
    chassi: str | None = None
    renavam: str | None = None
    marca_id: int | None = None
    modelo_id: int | None = None
    ano_fabricacao: int | None = None
    ano_modelo: int | None = None
    cor: str | None = None
    combustivel: str | None = None
    motorizacao: str | None = None
    observacoes: str | None = None
    situacao: str | None = None
    
    # 4.2.2 CLASSIFICAÇÃO
    prefixo: str | None = None
    tipo_frota_id: int | None = None
    categoria_id: int | None = None
    numero_patrimonio: str | None = None
    valor_aquisicao: float | None = None
    tipo_aquisicao: str | None = None
    tipo_convenio: str | None = None
    nome_locador: str | None = None
    valor_locacao: float | None = None
    
    # 4.2.3 ADMINISTRATIVA
    secretaria_id: int | None = None
    unidade_id: int | None = None
    subunidade_id: int | None = None
    centro_custo_id: int | None = None
    
    # 4.2.4 OPERACIONAL
    tipo_registro_id: int | None = None
    tipo_controle: str | None = None
    hodometro_horimetro_inicial: int | None = None
    capacidade_tanque: int | None = None
    capacidade_passageiros: int | None = None
    capacidade_carga: int | None = None
    
    # 4.2.5 DOCUMENTAÇÃO
    vencimento_licenciamento: date | None = None
    vencimento_seguro: date | None = None
    vencimento_ipva: date | None = None
    
    # 4.2.6 DADOS TÉCNICOS
    cilindrada: int | None = None
    potencia: int | None = None
    transmissao: str | None = None
    tracao: str | None = None
    vidros_eletricos: bool | None = None
    direcao: str | None = None
    ar_condicionado: bool | None = None
    pneu_dimensao: str | None = None
    pneu_velocidade: str | None = None
    pneu_carga: str | None = None
    
    # 4.2.7 LOCALIZAÇÃO
    uf: str | None = None
    municipio: str | None = None


class VeiculoResponse(VeiculoBase):
    """Response com todos os dados + relações."""
    id: int
    
    # Relações
    marca: MarcaResponse | None = None
    modelo: ModeloResponse | None = None
    tipo_veiculo: TipoVeiculoResponse | None = None
    tipo_frota: TipoFrotaResponse | None = None
    categoria: CategoriaResponse | None = None
    unidade: UnidadeResponse | None = None
    subunidade: SubunidadeResponse | None = None
    centro_custo: CentroCustoResponse | None = None

    model_config = {"from_attributes": True}


class VeiculoListItem(BaseModel):
    """Versão compacta para listagens."""
    id: int
    placa: str
    prefixo: str
    marca: MarcaResponse | None = None
    modelo: ModeloResponse | None = None
    ano_fabricacao: int
    situacao: str
    categoria: CategoriaResponse | None = None
    combustivel: str
    unidade: UnidadeResponse | None = None

    model_config = {"from_attributes": True}


# ── Documentos de Veículos ────────────────────────────────────────────

class DocumentoResponse(BaseModel):
    """Documento ou arquivo vinculado a um veículo (CRLV, foto, apólice, etc)."""
    id: int
    veiculo_id: int
    tipo: str
    descricao: str
    arquivo: str          # caminho relativo a MEDIA_DIR, ex: veiculos/ABC-1234/CRLV/uuid.pdf
    criado_em: datetime

    model_config = {"from_attributes": True}
