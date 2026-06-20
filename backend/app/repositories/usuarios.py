from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.usuarios import Secretaria, Usuario
from app.repositories.base import BaseRepository


class SecretariaRepository(BaseRepository[Secretaria]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Secretaria, session)

    async def get_ativas(self) -> list[Secretaria]:
        result = await self.session.execute(
            select(Secretaria).where(Secretaria.ativa == True).order_by(Secretaria.nome)
        )
        return list(result.scalars().all())


class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Usuario, session)

    async def get_by_username(self, username: str) -> Usuario | None:
        result = await self.session.execute(
            select(Usuario).where(Usuario.username == username)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Usuario | None:
        result = await self.session.execute(
            select(Usuario).where(Usuario.email == email)
        )
        return result.scalar_one_or_none()

    async def get_with_secretaria(self, user_id: int) -> Usuario | None:
        result = await self.session.execute(
            select(Usuario)
            .options(selectinload(Usuario.secretaria))
            .where(Usuario.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_all_with_secretaria(
        self, skip: int = 0, limit: int = 100
    ) -> list[Usuario]:
        result = await self.session.execute(
            select(Usuario)
            .options(selectinload(Usuario.secretaria))
            .offset(skip)
            .limit(limit)
            .order_by(Usuario.first_name, Usuario.last_name)
        )
        return list(result.scalars().all())
