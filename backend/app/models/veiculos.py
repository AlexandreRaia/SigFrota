from sqlalchemy import Boolean, ForeignKey, Integer, SmallInteger, String, Float, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


# ── Entidades Administrativas (Parametrizações)

class Categoria(Base):
    """Categoria de veículo: Passeio, Utilitário, Ambulância, etc."""
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(60), unique=True)
    descricao: Mapped[str] = mapped_column(String(250), default="")
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)

    veiculos: Mapped[list["Veiculo"]] = relationship(back_populates="categoria")

    def __repr__(self) -> str:
        return f"<Categoria {self.nome}>"


class TipoFrota(Base):
    """Tipo de frota: Próprio, Locado, Convênio, Cedido."""
    __tablename__ = "tipos_frota"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True)  # PROPRIO, LOCADO, CONVENIO, CEDIDO
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)

    veiculos: Mapped[list["Veiculo"]] = relationship(back_populates="tipo_frota_ref")

    def __repr__(self) -> str:
        return f"<TipoFrota {self.nome}>"


class Unidade(Base):
    """Unidades administrativas dentro de uma Secretaria."""
    __tablename__ = "unidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    secretaria_id: Mapped[int] = mapped_column(ForeignKey("secretarias.id"))
    nome: Mapped[str] = mapped_column(String(120))
    sigla: Mapped[str] = mapped_column(String(20), default="")
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)

    secretaria: Mapped["Secretaria"] = relationship(back_populates="unidades")
    subunidades: Mapped[list["Subunidade"]] = relationship(back_populates="unidade", cascade="all, delete-orphan")
    veiculos: Mapped[list["Veiculo"]] = relationship(back_populates="unidade")

    def __repr__(self) -> str:
        return f"<Unidade {self.nome}>"


class Subunidade(Base):
    """Subunidades dentro de uma Unidade."""
    __tablename__ = "subunidades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    unidade_id: Mapped[int] = mapped_column(ForeignKey("unidades.id"))
    nome: Mapped[str] = mapped_column(String(120))
    sigla: Mapped[str] = mapped_column(String(20), default="")
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)

    unidade: Mapped["Unidade"] = relationship(back_populates="subunidades")
    veiculos: Mapped[list["Veiculo"]] = relationship(back_populates="subunidade")

    def __repr__(self) -> str:
        return f"<Subunidade {self.nome}>"


class CentroCusto(Base):
    """Centros de custo para alocação de veículos."""
    __tablename__ = "centros_custo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True)
    nome: Mapped[str] = mapped_column(String(120))
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)

    veiculos: Mapped[list["Veiculo"]] = relationship(back_populates="centro_custo_ref")

    def __repr__(self) -> str:
        return f"<CentroCusto {self.codigo} - {self.nome}>"


class TipoVeiculo(Base):
    """Tipo de Registro: Veículo, Máquina, Equipamento."""
    __tablename__ = "tipos_veiculo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(50), unique=True)  # VEICULO, MAQUINA, EQUIPAMENTO
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    veiculos: Mapped[list["Veiculo"]] = relationship(back_populates="tipo_registro")

    def __repr__(self) -> str:
        return f"<TipoVeiculo {self.nome}>"


class Marca(Base):
    __tablename__ = "marcas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(60), unique=True)
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    modelos: Mapped[list["Modelo"]] = relationship(back_populates="marca", cascade="all, delete-orphan")
    veiculos: Mapped[list["Veiculo"]] = relationship(back_populates="marca")

    def __repr__(self) -> str:
        return f"<Marca {self.nome}>"


class Modelo(Base):
    __tablename__ = "modelos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    marca_id: Mapped[int] = mapped_column(ForeignKey("marcas.id"))
    nome: Mapped[str] = mapped_column(String(100))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    marca: Mapped["Marca"] = relationship(back_populates="modelos")
    veiculos: Mapped[list["Veiculo"]] = relationship(back_populates="modelo")

    def __repr__(self) -> str:
        return f"<Modelo {self.nome}>"


class Veiculo(Base, TimestampMixin):
    __tablename__ = "veiculos"

    # Status: ATIVO | INATIVO
    # TipoRegistro: VEICULO | MAQUINA | EQUIPAMENTO
    # TipoFrota: PROPRIO | LOCADO | CONVENIO | CEDIDO
    # Combustível: GASOLINA | DIESEL | FLEX | ELETRICO | GNV
    # TipoControle: QUILOMETRAGEM | HORIMETRO
    # Cor: lista de cores comuns

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ─── 4.2.1 DADOS GERAIS (Identificação)
    placa: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    chassi: Mapped[str] = mapped_column(String(17), unique=True)
    renavam: Mapped[str] = mapped_column(String(11), unique=True)
    marca_id: Mapped[int] = mapped_column(ForeignKey("marcas.id"))
    modelo_id: Mapped[int] = mapped_column(ForeignKey("modelos.id"))
    ano_fabricacao: Mapped[int] = mapped_column(SmallInteger)
    ano_modelo: Mapped[int] = mapped_column(SmallInteger)
    cor: Mapped[str] = mapped_column(String(30), default="")
    combustivel: Mapped[str] = mapped_column(String(12), default="FLEX")  # GASOLINA, DIESEL, FLEX, ELETRICO, GNV
    motorizacao: Mapped[str] = mapped_column(String(80), default="")  # Ex: 1.8 16V, 2.0 Diesel, etc.
    observacoes: Mapped[str] = mapped_column(String(500), default="")
    situacao: Mapped[str] = mapped_column(String(10), default="ATIVO")  # ATIVO | INATIVO

    # ─── 4.2.2 CLASSIFICAÇÃO DA FROTA
    prefixo: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    tipo_frota_id: Mapped[int] = mapped_column(ForeignKey("tipos_frota.id"))
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"))

    # ─── 4.2.3 VINCULAÇÃO ADMINISTRATIVA
    secretaria_id: Mapped[int] = mapped_column(ForeignKey("secretarias.id"))
    unidade_id: Mapped[int | None] = mapped_column(ForeignKey("unidades.id"), nullable=True)
    subunidade_id: Mapped[int | None] = mapped_column(ForeignKey("subunidades.id"), nullable=True)
    centro_custo_id: Mapped[int] = mapped_column(ForeignKey("centros_custo.id"))

    # ─── 4.2.4 DADOS OPERACIONAIS
    tipo_registro_id: Mapped[int] = mapped_column(ForeignKey("tipos_veiculo.id"))  # VEICULO | MAQUINA | EQUIPAMENTO
    tipo_controle: Mapped[str] = mapped_column(String(20), default="QUILOMETRAGEM")  # QUILOMETRAGEM | HORIMETRO
    hodometro_horimetro_inicial: Mapped[int] = mapped_column(Integer, default=0)
    capacidade_tanque: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Litros
    capacidade_passageiros: Mapped[int | None] = mapped_column(Integer, nullable=True)
    capacidade_carga: Mapped[int | None] = mapped_column(Integer, nullable=True)  # Em Kg

    # ─── 4.2.5 DOCUMENTAÇÃO BÁSICA (Vencimentos)
    vencimento_licenciamento: Mapped[str | None] = mapped_column(Date, nullable=True)
    vencimento_seguro: Mapped[str | None] = mapped_column(Date, nullable=True)

    # ─── 4.2.6 LOCALIZAÇÃO ADMINISTRATIVA
    uf: Mapped[str] = mapped_column(String(2), default="SP")
    municipio: Mapped[str] = mapped_column(String(120), default="")

    # ─── Relacionamentos
    marca: Mapped["Marca"] = relationship(back_populates="veiculos")
    modelo: Mapped["Modelo"] = relationship(back_populates="veiculos")
    tipo_registro: Mapped["TipoVeiculo"] = relationship(back_populates="veiculos")
    categoria: Mapped["Categoria"] = relationship(back_populates="veiculos")
    tipo_frota_ref: Mapped["TipoFrota"] = relationship(back_populates="veiculos", foreign_keys=[tipo_frota_id])
    secretaria: Mapped["Secretaria"] = relationship(back_populates="veiculos")
    unidade: Mapped["Unidade | None"] = relationship(back_populates="veiculos")
    subunidade: Mapped["Subunidade | None"] = relationship(back_populates="veiculos")
    centro_custo_ref: Mapped["CentroCusto"] = relationship(back_populates="veiculos")

    def __repr__(self) -> str:
        return f"<Veiculo {self.placa}>"
