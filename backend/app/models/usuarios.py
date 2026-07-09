from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Secretaria(Base, TimestampMixin):
    __tablename__ = "secretarias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(120))
    sigla: Mapped[str] = mapped_column(String(20))
    ativa: Mapped[bool] = mapped_column(Boolean, default=True)

    usuarios: Mapped[list["Usuario"]] = relationship(back_populates="secretaria")
    unidades: Mapped[list["Unidade"]] = relationship(back_populates="secretaria", cascade="all, delete-orphan")
    veiculos: Mapped[list["Veiculo"]] = relationship(back_populates="secretaria")

    def __repr__(self) -> str:
        return f"<Secretaria {self.sigla}>"


class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"

    # Perfis disponíveis: ADMIN | GESTOR | OPERADOR | OFICINA | AUDITOR

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(254), unique=True, index=True)
    first_name: Mapped[str] = mapped_column(String(150), default="")
    last_name: Mapped[str] = mapped_column(String(150), default="")
    hashed_password: Mapped[str] = mapped_column(String(128))

    perfil: Mapped[str] = mapped_column(String(10), default="OPERADOR")
    secretaria_id: Mapped[int | None] = mapped_column(
        ForeignKey("secretarias.id"), nullable=True
    )
    telefone: Mapped[str] = mapped_column(String(20), default="")
    foto: Mapped[str | None] = mapped_column(String(500), nullable=True)

    ativo: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    secretaria: Mapped["Secretaria | None"] = relationship(back_populates="usuarios")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def is_admin(self) -> bool:
        return self.perfil == "ADMIN" or self.is_superuser

    @property
    def is_gestor(self) -> bool:
        return self.perfil in ("ADMIN", "GESTOR") or self.is_superuser

    def __repr__(self) -> str:
        return f"<Usuario {self.username} ({self.perfil})>"
