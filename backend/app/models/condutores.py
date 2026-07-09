from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin

# Unidade e Subunidade são resolvidos via string pelo registry do SQLAlchemy


class Condutor(Base, TimestampMixin):
    __tablename__ = "condutores"

    # Status: ATIVO | INATIVO | SUSPENSO
    # CategoriaCNH: A | B | C | D | E | AB | AC | AD | AE | ACC

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Identificação
    prontuario: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(10), default="ATIVO", index=True)
    foto: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # ── Dados pessoais
    nome: Mapped[str] = mapped_column(String(160), index=True)
    data_nascimento: Mapped[date] = mapped_column(Date)
    cpf: Mapped[str] = mapped_column(String(14), unique=True, index=True)
    rg: Mapped[str] = mapped_column(String(20), default="")
    orgao_emissor: Mapped[str] = mapped_column(String(30), default="")
    cargo: Mapped[str] = mapped_column(String(100), default="")

    # ── Contato
    endereco: Mapped[str] = mapped_column(String(255), default="")
    telefone: Mapped[str] = mapped_column(String(20), default="")
    email: Mapped[str] = mapped_column(String(254), default="")

    # ── Lotação
    unidade_id: Mapped[int | None] = mapped_column(ForeignKey("unidades.id"), nullable=True)
    subunidade_id: Mapped[int | None] = mapped_column(ForeignKey("subunidades.id"), nullable=True)

    # ── CNH
    cnh_categoria: Mapped[str] = mapped_column(String(3), default="")
    cnh_numero: Mapped[str] = mapped_column(String(11), default="")
    cnh_emissao: Mapped[date | None] = mapped_column(Date, nullable=True)
    cnh_vencimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    cnh_orgao: Mapped[str] = mapped_column(String(30), default="")
    cnh_arquivo: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # ── Relacionamentos
    unidade: Mapped["Unidade | None"] = relationship("Unidade", foreign_keys=[unidade_id], lazy="noload")  # type: ignore[name-defined]
    subunidade: Mapped["Subunidade | None"] = relationship("Subunidade", foreign_keys=[subunidade_id], lazy="noload")  # type: ignore[name-defined]
    documentos: Mapped[list["CondutorDocumento"]] = relationship(back_populates="condutor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Condutor {self.nome} ({self.cpf})>"


class CondutorDocumento(Base, TimestampMixin):
    """Documentos e fotos anexados a um condutor (CNH, foto, etc)."""
    __tablename__ = "condutor_documentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    condutor_id: Mapped[int] = mapped_column(ForeignKey("condutores.id"), index=True)

    # FOTO, CNH, OUTRO
    tipo: Mapped[str] = mapped_column(String(30))

    # Caminho relativo a MEDIA_DIR
    arquivo: Mapped[str] = mapped_column(String(255))

    # Descrição opcional
    descricao: Mapped[str] = mapped_column(String(200), default="")

    condutor: Mapped["Condutor"] = relationship(back_populates="documentos")

    def __repr__(self) -> str:
        return f"<CondutorDocumento {self.tipo} - {self.arquivo}>"
