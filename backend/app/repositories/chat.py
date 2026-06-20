from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.chat import SMVMensagem, SMVMensagemLeitura
from app.repositories.base import BaseRepository


class SMVMensagemRepository(BaseRepository[SMVMensagem]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(SMVMensagem, session)

    async def get_por_smv(self, smv_id: int) -> list[SMVMensagem]:
        result = await self.session.execute(
            select(SMVMensagem)
            .options(selectinload(SMVMensagem.autor))
            .where(SMVMensagem.smv_id == smv_id)
            .order_by(SMVMensagem.enviada_em)
        )
        return list(result.scalars().all())

    async def contar_nao_lidas(self, smv_id: int, usuario_id: int) -> int:
        lidas_subq = (
            select(SMVMensagemLeitura.mensagem_id)
            .where(SMVMensagemLeitura.usuario_id == usuario_id)
            .scalar_subquery()
        )
        result = await self.session.execute(
            select(SMVMensagem)
            .where(
                and_(
                    SMVMensagem.smv_id == smv_id,
                    SMVMensagem.id.not_in(lidas_subq),
                )
            )
        )
        return len(result.scalars().all())

    async def marcar_lidas(self, smv_id: int, usuario_id: int) -> None:
        mensagens = await self.get_por_smv(smv_id)
        for msg in mensagens:
            existe = await self.session.execute(
                select(SMVMensagemLeitura).where(
                    and_(
                        SMVMensagemLeitura.mensagem_id == msg.id,
                        SMVMensagemLeitura.usuario_id == usuario_id,
                    )
                )
            )
            if not existe.scalar_one_or_none():
                leitura = SMVMensagemLeitura(mensagem_id=msg.id, usuario_id=usuario_id)
                self.session.add(leitura)
        await self.session.commit()
