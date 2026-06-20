from datetime import datetime

from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


async def _proximo_numero_smv(session: AsyncSession) -> str:
    """Gera número sequencial no formato ANO-NNNN (ex: 2026-0001)."""
    from sqlalchemy import text

    ano = datetime.now().year
    result = await session.execute(
        text(
            "SELECT numero FROM smvs WHERE numero LIKE :prefix ORDER BY numero DESC LIMIT 1 FOR UPDATE"
        ),
        {"prefix": f"{ano}-%"},
    )
    row = result.fetchone()
    if row:
        seq = int(row[0].split("-")[1]) + 1
    else:
        seq = 1
    return f"{ano}-{seq:04d}"


class SMV(Base, TimestampMixin):
    __tablename__ = "smvs"

    # Etapas: SOLICITACAO | RECEPCAO | DIAGNOSTICO | ORCAMENTO | APROVACAO
    #         EXECUCAO | RETIRADA | EMISSAO_NF | FINALIZADO
    # Urgência: BAIXA | MEDIA | ALTA

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    numero: Mapped[str] = mapped_column(String(10), unique=True, index=True)

    veiculo_id: Mapped[int] = mapped_column(ForeignKey("veiculos.id"))
    solicitante_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    etapa: Mapped[str] = mapped_column(String(15), default="SOLICITACAO", index=True)
    urgencia: Mapped[str] = mapped_column(String(10), default="MEDIA")

    descricao_problema: Mapped[str] = mapped_column(Text)
    km_entrada: Mapped[int | None] = mapped_column(Integer, nullable=True)
    km_saida: Mapped[int | None] = mapped_column(Integer, nullable=True)

    diagnostico: Mapped[str] = mapped_column(Text, default="")
    tipos_servico: Mapped[str] = mapped_column(String(300), default="")

    # Datas de controle por etapa
    dt_solicitacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    dt_recepcao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    dt_diagnostico: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    dt_inicio_exec: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    dt_retirada: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    dt_finalizacao: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    observacoes: Mapped[str] = mapped_column(Text, default="")

    # ── Relacionamentos
    veiculo: Mapped["Veiculo"] = relationship()  # type: ignore[name-defined]
    solicitante: Mapped["Usuario"] = relationship()  # type: ignore[name-defined]
    historico_etapas: Mapped[list["SMVEtapa"]] = relationship(
        back_populates="smv", order_by="SMVEtapa.data"
    )
    orcamentos: Mapped[list["SMVOrcamento"]] = relationship(back_populates="smv")
    itens_diagnostico: Mapped[list["SMVDiagnosticoItem"]] = relationship(back_populates="smv")
    anexos: Mapped[list["SMVAnexo"]] = relationship(back_populates="smv")
    notas_fiscais: Mapped[list["SMVNotaFiscal"]] = relationship(back_populates="smv")
    mensagens: Mapped[list["SMVMensagem"]] = relationship(back_populates="smv")

    def __repr__(self) -> str:
        return f"<SMV {self.numero}>"


class SMVEtapa(Base):
    __tablename__ = "smv_etapas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    smv_id: Mapped[int] = mapped_column(ForeignKey("smvs.id"))
    etapa_de: Mapped[str] = mapped_column(String(15), default="")
    etapa_para: Mapped[str] = mapped_column(String(15))
    responsavel_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    observacao: Mapped[str] = mapped_column(Text, default="")
    data: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    smv: Mapped["SMV"] = relationship(back_populates="historico_etapas")
    responsavel: Mapped["Usuario"] = relationship()  # type: ignore[name-defined]


class SMVDiagnosticoItem(Base):
    __tablename__ = "smv_diagnostico_itens"

    # Tipo: PECA | SERVICO

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    smv_id: Mapped[int] = mapped_column(ForeignKey("smvs.id"))
    tipo: Mapped[str] = mapped_column(String(10), default="PECA")
    descricao: Mapped[str] = mapped_column(String(300))
    quantidade: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=1)
    valor_unitario: Mapped[Decimal | None] = mapped_column(Numeric(12, 2), nullable=True)

    smv: Mapped["SMV"] = relationship(back_populates="itens_diagnostico")


class SMVOrcamento(Base, TimestampMixin):
    __tablename__ = "smv_orcamentos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    smv_id: Mapped[int] = mapped_column(ForeignKey("smvs.id"))
    criado_por_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    fornecedor: Mapped[str] = mapped_column(String(200), default="")
    valor_mao_obra: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    valor_pecas: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    valor_total: Mapped[Decimal] = mapped_column(Numeric(12, 2), default=0)
    aprovado: Mapped[bool | None] = mapped_column(nullable=True)
    observacao: Mapped[str] = mapped_column(Text, default="")
    arquivo: Mapped[str | None] = mapped_column(String(500), nullable=True)

    smv: Mapped["SMV"] = relationship(back_populates="orcamentos")
    criado_por: Mapped["Usuario"] = relationship()  # type: ignore[name-defined]


class SMVAnexo(Base, TimestampMixin):
    __tablename__ = "smv_anexos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    smv_id: Mapped[int] = mapped_column(ForeignKey("smvs.id"))
    enviado_por_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    arquivo: Mapped[str] = mapped_column(String(500))
    descricao: Mapped[str] = mapped_column(String(200), default="")

    smv: Mapped["SMV"] = relationship(back_populates="anexos")
    enviado_por: Mapped["Usuario"] = relationship()  # type: ignore[name-defined]


class SMVNotaFiscal(Base, TimestampMixin):
    __tablename__ = "smv_notas_fiscais"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    smv_id: Mapped[int] = mapped_column(ForeignKey("smvs.id"))
    numero_nf: Mapped[str] = mapped_column(String(50))
    fornecedor: Mapped[str] = mapped_column(String(200))
    valor_total: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    arquivo: Mapped[str | None] = mapped_column(String(500), nullable=True)

    smv: Mapped["SMV"] = relationship(back_populates="notas_fiscais")
    itens: Mapped[list["SMVItemNF"]] = relationship(back_populates="nota_fiscal")


class SMVItemNF(Base):
    __tablename__ = "smv_itens_nf"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nota_fiscal_id: Mapped[int] = mapped_column(ForeignKey("smv_notas_fiscais.id"))
    descricao: Mapped[str] = mapped_column(String(300))
    quantidade: Mapped[Decimal] = mapped_column(Numeric(8, 2), default=1)
    valor_unitario: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    valor_total: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    nota_fiscal: Mapped["SMVNotaFiscal"] = relationship(back_populates="itens")
