from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.condutores import Condutor, CondutorDocumento
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

    async def get_com_relacoes(self, condutor_id: int) -> Condutor | None:
        result = await self.session.execute(
            select(Condutor)
            .options(
                selectinload(Condutor.unidade),
                selectinload(Condutor.subunidade),
            )
            .where(Condutor.id == condutor_id)
        )
        return result.scalar_one_or_none()

    async def search(
        self,
        q: str = "",
        status: str = "",
        unidade_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Condutor]:
        stmt = select(Condutor).options(
            selectinload(Condutor.unidade),
            selectinload(Condutor.subunidade),
        )
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
        if unidade_id:
            filters.append(Condutor.unidade_id == unidade_id)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.offset(skip).limit(limit).order_by(Condutor.nome)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


class CondutorDocumentoRepository(BaseRepository[CondutorDocumento]):
    """Repository para documentos e fotos vinculados a condutores."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(CondutorDocumento, session)

    async def listar_por_condutor(self, condutor_id: int) -> list[CondutorDocumento]:
        result = await self.session.execute(
            select(CondutorDocumento)
            .where(CondutorDocumento.condutor_id == condutor_id)
            .order_by(CondutorDocumento.criado_em.desc())
        )
        return list(result.scalars().all())
