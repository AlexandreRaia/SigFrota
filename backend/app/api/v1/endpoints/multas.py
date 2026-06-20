from fastapi import APIRouter, Depends, Query

from app.core.dependencies import DatabaseDep, get_current_user, require_perfil
from app.repositories.multas import MultaRepository, TipoMultaRepository
from app.schemas.common import MessageResponse
from app.schemas.multas import MultaCreate, MultaListItem, MultaResponse, MultaUpdate, TipoMultaResponse
from app.services.multas import MultaService

router = APIRouter(prefix="/multas", tags=["Multas"])


@router.get("/tipos", response_model=list[TipoMultaResponse], dependencies=[Depends(get_current_user)])
async def listar_tipos_multa(db: DatabaseDep):
    return await TipoMultaRepository(db).get_ativos()


@router.get("", response_model=list[MultaListItem], dependencies=[Depends(get_current_user)])
async def listar_multas(
    db: DatabaseDep,
    q: str = Query("", description="Busca por placa"),
    status: str = Query(""),
    condutor_id: int | None = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    return await MultaRepository(db).search(q=q, status=status, condutor_id=condutor_id, skip=skip, limit=limit)


@router.post("", response_model=MultaResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_multa(data: MultaCreate, db: DatabaseDep):
    service = MultaService(MultaRepository(db))
    return await service.criar(data)


@router.get("/{multa_id}", response_model=MultaResponse, dependencies=[Depends(get_current_user)])
async def detalhe_multa(multa_id: int, db: DatabaseDep):
    service = MultaService(MultaRepository(db))
    return await service.get_or_404(multa_id)


@router.patch("/{multa_id}", response_model=MultaResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_multa(multa_id: int, data: MultaUpdate, db: DatabaseDep):
    service = MultaService(MultaRepository(db))
    return await service.atualizar(multa_id, data)


@router.delete("/{multa_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_multa(multa_id: int, db: DatabaseDep):
    service = MultaService(MultaRepository(db))
    multa = await service.get_or_404(multa_id)
    await MultaRepository(db).delete(multa)
    return MessageResponse(message="Multa excluída com sucesso")
