from datetime import date

from decimal import Decimal

from sqlalchemy import Boolean, Date, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class TipoMulta(Base):
    __tablename__ = "tipos_multa"

    # Natureza: LEVE | MEDIA | GRAVE | GRAVISSIMA

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    descricao: Mapped[str] = mapped_column(String(200))
    natureza: Mapped[str] = mapped_column(String(12))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    multas: Mapped[list["Multa"]] = relationship(back_populates="tipo_infracao")

    def __repr__(self) -> str:
        return f"<TipoMulta {self.codigo}>"


class Multa(Base, TimestampMixin):
    __tablename__ = "multas"

    # Status: PENDENTE | PAGA | CONTESTADA | VENCIDA

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    placa: Mapped[str] = mapped_column(String(10), index=True)
    condutor_id: Mapped[int | None] = mapped_column(ForeignKey("condutores.id"), nullable=True)
    tipo_infracao_id: Mapped[int | None] = mapped_column(
        ForeignKey("tipos_multa.id"), nullable=True
    )

    pontos: Mapped[int] = mapped_column(Integer, default=0)
    valor: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    data_infracao: Mapped[date] = mapped_column(Date, index=True)

    status: Mapped[str] = mapped_column(String(12), default="PENDENTE", index=True)
    data_vencimento: Mapped[date] = mapped_column(Date)
    prazo_indicacao: Mapped[date | None] = mapped_column(Date, nullable=True)
    prazo_defesa: Mapped[date | None] = mapped_column(Date, nullable=True)

    arquivo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    observacao: Mapped[str] = mapped_column(Text, default="")

    # ── Relacionamentos
    condutor: Mapped["Condutor | None"] = relationship()  # type: ignore[name-defined]
    tipo_infracao: Mapped["TipoMulta | None"] = relationship(back_populates="multas")

    def __repr__(self) -> str:
        return f"<Multa {self.placa} {self.data_infracao}>"
