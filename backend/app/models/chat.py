from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class SMVMensagem(Base):
    __tablename__ = "smv_mensagens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    smv_id: Mapped[int] = mapped_column(ForeignKey("smvs.id"), index=True)
    etapa: Mapped[str] = mapped_column(String(15))
    autor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    texto: Mapped[str] = mapped_column(Text, default="")
    anexo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    enviada_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )

    smv: Mapped["SMV"] = relationship("SMV", back_populates="mensagens")  # type: ignore[name-defined]
    autor: Mapped["Usuario"] = relationship()  # type: ignore[name-defined]
    leituras: Mapped[list["SMVMensagemLeitura"]] = relationship(back_populates="mensagem")

    def __repr__(self) -> str:
        return f"<SMVMensagem smv={self.smv_id} autor={self.autor_id}>"


class SMVMensagemLeitura(Base):
    __tablename__ = "smv_mensagens_leitura"

    __table_args__ = (UniqueConstraint("mensagem_id", "usuario_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    mensagem_id: Mapped[int] = mapped_column(ForeignKey("smv_mensagens.id"), index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    lida_em: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    mensagem: Mapped["SMVMensagem"] = relationship(back_populates="leituras")
