from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError

from app.core.dependencies import DatabaseDep, get_current_user, require_perfil
from app.models.veiculos import CentroCusto, Subunidade, Unidade
from app.repositories.veiculos import (
    CentroCustoRepository,
    SubunidadeRepository,
    UnidadeRepository,
)
from app.schemas.common import MessageResponse
from app.schemas.veiculos import (
    CentroCustoCreate,
    CentroCustoResponse,
    CentroCustoUpdate,
    SubunidadeCreate,
    SubunidadeResponse,
    SubunidadeUpdate,
    UnidadeCreate,
    UnidadeResponse,
    UnidadeUpdate,
)

router = APIRouter(prefix="/parametrizacoes", tags=["Parametrizações"])


# ── Unidades ────────────────────────────────────────────────────────────────

@router.get("/unidades", response_model=list[UnidadeResponse], dependencies=[Depends(get_current_user)])
async def listar_unidades(
    db: DatabaseDep,
    secretaria_id: int | None = Query(None),
):
    """Listar unidades (ativas e inativas) para gestão."""
    repo = UnidadeRepository(db)
    unidades = await repo.get_all(limit=1000)
    if secretaria_id is not None:
        unidades = [u for u in unidades if u.secretaria_id == secretaria_id]
    return sorted(unidades, key=lambda u: u.nome.lower())


@router.post("/unidades", response_model=UnidadeResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_unidade(data: UnidadeCreate, db: DatabaseDep):
    """Criar uma nova unidade."""
    repo = UnidadeRepository(db)
    return await repo.create(Unidade(**data.model_dump()))


@router.patch("/unidades/{unidade_id}", response_model=UnidadeResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_unidade(unidade_id: int, data: UnidadeUpdate, db: DatabaseDep):
    """Atualizar uma unidade."""
    repo = UnidadeRepository(db)
    unidade = await repo.get_by_id(unidade_id)
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")
    return await repo.update(unidade, data.model_dump(exclude_unset=True))


@router.delete("/unidades/{unidade_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_unidade(unidade_id: int, db: DatabaseDep):
    """Excluir uma unidade."""
    repo = UnidadeRepository(db)
    unidade = await repo.get_by_id(unidade_id)
    if not unidade:
        raise HTTPException(status_code=404, detail="Unidade não encontrada")
    try:
        await repo.delete(unidade)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: há veículos vinculados a esta unidade. Inative-a.",
        )
    return MessageResponse(message="Unidade excluída com sucesso")


# ── Subunidades ───────────────────────────────────────────────────────────────

@router.get("/subunidades", response_model=list[SubunidadeResponse], dependencies=[Depends(get_current_user)])
async def listar_subunidades(
    db: DatabaseDep,
    unidade_id: int | None = Query(None),
):
    """Listar subunidades (ativas e inativas) para gestão."""
    repo = SubunidadeRepository(db)
    subunidades = await repo.get_all(limit=1000)
    if unidade_id is not None:
        subunidades = [s for s in subunidades if s.unidade_id == unidade_id]
    return sorted(subunidades, key=lambda s: s.nome.lower())


@router.post("/subunidades", response_model=SubunidadeResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_subunidade(data: SubunidadeCreate, db: DatabaseDep):
    """Criar uma nova subunidade."""
    repo = SubunidadeRepository(db)
    return await repo.create(Subunidade(**data.model_dump()))


@router.patch("/subunidades/{subunidade_id}", response_model=SubunidadeResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_subunidade(subunidade_id: int, data: SubunidadeUpdate, db: DatabaseDep):
    """Atualizar uma subunidade."""
    repo = SubunidadeRepository(db)
    subunidade = await repo.get_by_id(subunidade_id)
    if not subunidade:
        raise HTTPException(status_code=404, detail="Subunidade não encontrada")
    return await repo.update(subunidade, data.model_dump(exclude_unset=True))


@router.delete("/subunidades/{subunidade_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_subunidade(subunidade_id: int, db: DatabaseDep):
    """Excluir uma subunidade."""
    repo = SubunidadeRepository(db)
    subunidade = await repo.get_by_id(subunidade_id)
    if not subunidade:
        raise HTTPException(status_code=404, detail="Subunidade não encontrada")
    try:
        await repo.delete(subunidade)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: há veículos vinculados a esta subunidade. Inative-a.",
        )
    return MessageResponse(message="Subunidade excluída com sucesso")


# ── Centros de Custo ──────────────────────────────────────────────────────────

@router.get("/centros-custo", response_model=list[CentroCustoResponse], dependencies=[Depends(get_current_user)])
async def listar_centros_custo(db: DatabaseDep):
    """Listar centros de custo (ativos e inativos) para gestão."""
    repo = CentroCustoRepository(db)
    centros = await repo.get_all(limit=1000)
    return sorted(centros, key=lambda c: c.codigo.lower())


@router.post("/centros-custo", response_model=CentroCustoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_centro_custo(data: CentroCustoCreate, db: DatabaseDep):
    """Criar um novo centro de custo."""
    repo = CentroCustoRepository(db)
    try:
        return await repo.create(CentroCusto(**data.model_dump()))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um centro de custo com este código.")


@router.patch("/centros-custo/{centro_custo_id}", response_model=CentroCustoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_centro_custo(centro_custo_id: int, data: CentroCustoUpdate, db: DatabaseDep):
    """Atualizar um centro de custo."""
    repo = CentroCustoRepository(db)
    centro = await repo.get_by_id(centro_custo_id)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro de custo não encontrado")
    try:
        return await repo.update(centro, data.model_dump(exclude_unset=True))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um centro de custo com este código.")


@router.delete("/centros-custo/{centro_custo_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_centro_custo(centro_custo_id: int, db: DatabaseDep):
    """Excluir um centro de custo."""
    repo = CentroCustoRepository(db)
    centro = await repo.get_by_id(centro_custo_id)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro de custo não encontrado")
    try:
        await repo.delete(centro)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: há veículos vinculados a este centro de custo. Inative-o.",
        )
    return MessageResponse(message="Centro de custo excluído com sucesso")
