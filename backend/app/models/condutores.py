from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


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
    secretaria_id: Mapped[int] = mapped_column(ForeignKey("secretarias.id"))
    unidade: Mapped[str] = mapped_column(String(100), default="")

    # ── CNH
    cnh_categoria: Mapped[str] = mapped_column(String(3), default="")
    cnh_numero: Mapped[str] = mapped_column(String(11), default="")
    cnh_emissao: Mapped[date | None] = mapped_column(Date, nullable=True)
    cnh_vencimento: Mapped[date | None] = mapped_column(Date, nullable=True)
    cnh_orgao: Mapped[str] = mapped_column(String(30), default="")
    cnh_arquivo: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # ── Relacionamentos
    secretaria: Mapped["Secretaria"] = relationship(back_populates="condutores")  # type: ignore[name-defined]

    def __repr__(self) -> str:
        return f"<Condutor {self.nome} ({self.cpf})>"
