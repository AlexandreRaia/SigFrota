from fastapi import APIRouter, Depends

from app.core.dependencies import DatabaseDep, get_current_user
from app.repositories.chat import SMVMensagemRepository
from app.schemas.chat import MarcarLidaRequest, MensagemCreate, MensagemResponse
from app.services.manutencao import SMVService
from app.repositories.manutencao import SMVRepository

router = APIRouter(prefix="/chat", tags=["Chat / Mensagens"])


@router.get("/smv/{smv_id}", response_model=list[MensagemResponse])
async def listar_mensagens(smv_id: int, db: DatabaseDep, current_user=Depends(get_current_user)):
    smv_service = SMVService(SMVRepository(db))
    await smv_service.get_or_404(smv_id)
    repo = SMVMensagemRepository(db)
    mensagens = await repo.get_por_smv(smv_id)
    # Marcar como lidas automaticamente
    await repo.marcar_lidas(smv_id, current_user.id)
    return mensagens


@router.post("/smv/{smv_id}", response_model=MensagemResponse)
async def enviar_mensagem(smv_id: int, data: MensagemCreate, db: DatabaseDep, current_user=Depends(get_current_user)):
    from app.models.chat import SMVMensagem
    smv_service = SMVService(SMVRepository(db))
    smv = await smv_service.get_or_404(smv_id)
    mensagem = SMVMensagem(
        smv_id=smv_id,
        etapa=smv.etapa,
        autor_id=current_user.id,
        texto=data.texto,
    )
    db.add(mensagem)
    await db.commit()
    await db.refresh(mensagem)
    return mensagem


@router.get("/smv/{smv_id}/nao-lidas", response_model=dict)
async def contar_nao_lidas(smv_id: int, db: DatabaseDep, current_user=Depends(get_current_user)):
    repo = SMVMensagemRepository(db)
    count = await repo.contar_nao_lidas(smv_id, current_user.id)
    return {"smv_id": smv_id, "nao_lidas": count}
