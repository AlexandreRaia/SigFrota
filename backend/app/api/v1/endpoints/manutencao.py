from fastapi import APIRouter, Depends, Query

from app.core.dependencies import DatabaseDep, get_current_user, require_perfil
from app.repositories.manutencao import SMVRepository
from app.schemas.common import MessageResponse
from app.schemas.manutencao import (
    SMVAvancarEtapa,
    SMVCreate,
    SMVDetalheResponse,
    SMVDiagnosticoItemCreate,
    SMVDiagnosticoItemResponse,
    SMVListItem,
    SMVOrcamentoCreate,
    SMVOrcamentoResponse,
    SMVResponse,
    SMVUpdate,
)
from app.services.manutencao import SMVService

router = APIRouter(prefix="/manutencao", tags=["Manutenção"])


@router.get("", response_model=list[SMVListItem], dependencies=[Depends(get_current_user)])
async def listar_smvs(
    db: DatabaseDep,
    q: str = Query(""),
    etapa: str = Query(""),
    urgencia: str = Query(""),
    skip: int = 0,
    limit: int = 100,
):
    return await SMVRepository(db).search(q=q, etapa=etapa, urgencia=urgencia, skip=skip, limit=limit)


@router.post("", response_model=SMVResponse)
async def criar_smv(data: SMVCreate, db: DatabaseDep, current_user=Depends(get_current_user)):
    service = SMVService(SMVRepository(db))
    return await service.criar(data, current_user)


@router.get("/dashboard")
async def dashboard_manutencao(db: DatabaseDep, _=Depends(get_current_user)):
    repo = SMVRepository(db)
    contagens = await repo.count_by_etapa()
    total = sum(contagens.values())
    em_aberto = total - contagens.get("FINALIZADO", 0)
    return {
        "total": total,
        "em_aberto": em_aberto,
        "finalizadas": contagens.get("FINALIZADO", 0),
        "por_etapa": contagens,
    }


@router.get("/{smv_id}", response_model=SMVDetalheResponse, dependencies=[Depends(get_current_user)])
async def detalhe_smv(smv_id: int, db: DatabaseDep):
    service = SMVService(SMVRepository(db))
    return await service.get_or_404(smv_id)


@router.patch("/{smv_id}", response_model=SMVResponse, dependencies=[Depends(get_current_user)])
async def atualizar_smv(smv_id: int, data: SMVUpdate, db: DatabaseDep):
    from fastapi import HTTPException, status
    repo = SMVRepository(db)
    smv = await repo.get_by_id(smv_id)
    if not smv:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SMV não encontrada")
    return await repo.update(smv, data.model_dump(exclude_none=True))


@router.post("/{smv_id}/avancar", response_model=SMVResponse)
async def avancar_etapa(smv_id: int, data: SMVAvancarEtapa, db: DatabaseDep, current_user=Depends(get_current_user)):
    service = SMVService(SMVRepository(db))
    return await service.avancar_etapa(smv_id, data, current_user)


@router.post("/{smv_id}/orcamentos", response_model=SMVOrcamentoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR", "OFICINA"))])
async def adicionar_orcamento(smv_id: int, data: SMVOrcamentoCreate, db: DatabaseDep, current_user=Depends(get_current_user)):
    from decimal import Decimal
    from app.models.manutencao import SMVOrcamento
    service = SMVService(SMVRepository(db))
    smv = await service.get_or_404(smv_id)
    valor_total = data.valor_mao_obra + data.valor_pecas
    orcamento = SMVOrcamento(
        smv_id=smv.id,
        criado_por_id=current_user.id,
        fornecedor=data.fornecedor,
        valor_mao_obra=data.valor_mao_obra,
        valor_pecas=data.valor_pecas,
        valor_total=valor_total,
        observacao=data.observacao,
    )
    db.add(orcamento)
    await db.commit()
    await db.refresh(orcamento)
    return orcamento


@router.post("/{smv_id}/diagnostico", response_model=SMVDiagnosticoItemResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR", "OFICINA"))])
async def adicionar_item_diagnostico(smv_id: int, data: SMVDiagnosticoItemCreate, db: DatabaseDep):
    from app.models.manutencao import SMVDiagnosticoItem
    service = SMVService(SMVRepository(db))
    smv = await service.get_or_404(smv_id)
    item = SMVDiagnosticoItem(smv_id=smv.id, **data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item
