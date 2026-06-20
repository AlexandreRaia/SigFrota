from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.condutores import Condutor
from app.repositories.base import BaseRepository


class CondutorRepository(BaseRepository[Condutor]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Condutor, session)

    async def get_by_cpf(self, cpf: str) -> Condutor | None:
        result = await self.session.execute(
            select(Condutor).where(Condutor.cpf == cpf)
        )
        return result.scalar_one_or_none()

    async def get_by_prontuario(self, prontuario: str) -> Condutor | None:
        result = await self.session.execute(
            select(Condutor).where(Condutor.prontuario == prontuario)
        )
        return result.scalar_one_or_none()

    async def search(
        self,
        q: str = "",
        status: str = "",
        secretaria_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Condutor]:
        stmt = select(Condutor).options(selectinload(Condutor.secretaria))
        filters = []
        if q:
            filters.append(
                or_(
                    Condutor.nome.ilike(f"%{q}%"),
                    Condutor.cpf.ilike(f"%{q}%"),
                    Condutor.prontuario.ilike(f"%{q}%"),
                )
            )
        if status:
            filters.append(Condutor.status == status)
        if secretaria_id:
            filters.append(Condutor.secretaria_id == secretaria_id)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.offset(skip).limit(limit).order_by(Condutor.nome)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
