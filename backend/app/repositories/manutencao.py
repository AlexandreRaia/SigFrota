from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.manutencao import SMV, SMVEtapa, SMVOrcamento
from app.repositories.base import BaseRepository


class SMVRepository(BaseRepository[SMV]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(SMV, session)

    async def get_by_numero(self, numero: str) -> SMV | None:
        result = await self.session.execute(
            select(SMV).where(SMV.numero == numero)
        )
        return result.scalar_one_or_none()

    async def get_detalhe(self, smv_id: int) -> SMV | None:
        result = await self.session.execute(
            select(SMV)
            .options(
                selectinload(SMV.historico_etapas),
                selectinload(SMV.orcamentos),
                selectinload(SMV.itens_diagnostico),
                selectinload(SMV.anexos),
            )
            .where(SMV.id == smv_id)
        )
        return result.scalar_one_or_none()

    async def search(
        self,
        q: str = "",
        etapa: str = "",
        urgencia: str = "",
        veiculo_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[SMV]:
        stmt = select(SMV)
        filters = []
        if q:
            filters.append(SMV.numero.ilike(f"%{q}%"))
        if etapa:
            filters.append(SMV.etapa == etapa)
        if urgencia:
            filters.append(SMV.urgencia == urgencia)
        if veiculo_id:
            filters.append(SMV.veiculo_id == veiculo_id)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.offset(skip).limit(limit).order_by(SMV.numero.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count_by_etapa(self) -> dict[str, int]:
        result = await self.session.execute(
            select(SMV.etapa, func.count(SMV.id)).group_by(SMV.etapa)
        )
        return dict(result.all())

    async def proximo_numero(self) -> str:
        from datetime import datetime

        ano = datetime.now().year
        result = await self.session.execute(
            select(SMV.numero)
            .where(SMV.numero.like(f"{ano}-%"))
            .order_by(SMV.numero.desc())
            .limit(1)
            .with_for_update()
        )
        row = result.scalar_one_or_none()
        if row:
            seq = int(row.split("-")[1]) + 1
        else:
            seq = 1
        return f"{ano}-{seq:04d}"
