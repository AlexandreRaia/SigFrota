from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.multas import Multa, TipoMulta
from app.repositories.base import BaseRepository


class TipoMultaRepository(BaseRepository[TipoMulta]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(TipoMulta, session)

    async def get_ativos(self) -> list[TipoMulta]:
        result = await self.session.execute(
            select(TipoMulta).where(TipoMulta.ativo == True).order_by(TipoMulta.codigo)
        )
        return list(result.scalars().all())


class MultaRepository(BaseRepository[Multa]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Multa, session)

    async def search(
        self,
        q: str = "",
        status: str = "",
        condutor_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Multa]:
        stmt = select(Multa).options(selectinload(Multa.tipo_infracao))
        filters = []
        if q:
            filters.append(Multa.placa.ilike(f"%{q}%"))
        if status:
            filters.append(Multa.status == status)
        if condutor_id:
            filters.append(Multa.condutor_id == condutor_id)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.offset(skip).limit(limit).order_by(Multa.data_infracao.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
