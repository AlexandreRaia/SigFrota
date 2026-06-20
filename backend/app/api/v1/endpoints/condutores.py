from fastapi import APIRouter, Depends, Query

from app.core.dependencies import DatabaseDep, get_current_user, require_perfil
from app.repositories.condutores import CondutorRepository
from app.schemas.common import MessageResponse
from app.schemas.condutores import CondutorCreate, CondutorListItem, CondutorResponse, CondutorUpdate
from app.services.condutores import CondutorService

router = APIRouter(prefix="/condutores", tags=["Condutores"])


@router.get("", response_model=list[CondutorListItem], dependencies=[Depends(get_current_user)])
async def listar_condutores(
    db: DatabaseDep,
    q: str = Query(""),
    status: str = Query(""),
    secretaria_id: int | None = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    return await CondutorRepository(db).search(q=q, status=status, secretaria_id=secretaria_id, skip=skip, limit=limit)


@router.post("", response_model=CondutorResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_condutor(data: CondutorCreate, db: DatabaseDep):
    service = CondutorService(CondutorRepository(db))
    return await service.criar(data)


@router.get("/{condutor_id}", response_model=CondutorResponse, dependencies=[Depends(get_current_user)])
async def detalhe_condutor(condutor_id: int, db: DatabaseDep):
    service = CondutorService(CondutorRepository(db))
    return await service.get_or_404(condutor_id)


@router.patch("/{condutor_id}", response_model=CondutorResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_condutor(condutor_id: int, data: CondutorUpdate, db: DatabaseDep):
    service = CondutorService(CondutorRepository(db))
    return await service.atualizar(condutor_id, data)


@router.delete("/{condutor_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_condutor(condutor_id: int, db: DatabaseDep):
    service = CondutorService(CondutorRepository(db))
    condutor = await service.get_or_404(condutor_id)
    await CondutorRepository(db).delete(condutor)
    return MessageResponse(message="Condutor excluído com sucesso")
