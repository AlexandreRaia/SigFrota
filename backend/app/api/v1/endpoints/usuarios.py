from fastapi import APIRouter, Depends

from app.core.dependencies import DatabaseDep, get_current_user, require_perfil
from app.repositories.usuarios import SecretariaRepository, UsuarioRepository
from app.schemas.common import MessageResponse
from app.schemas.usuarios import (
    SecretariaCreate,
    SecretariaResponse,
    SecretariaUpdate,
    UsuarioChangePassword,
    UsuarioCreate,
    UsuarioResponse,
    UsuarioUpdate,
)
from app.services.usuarios import UsuarioService

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


# ── Secretarias ────────────────────────────────────────────────────────────────

@router.get("/secretarias", response_model=list[SecretariaResponse])
async def listar_secretarias(db: DatabaseDep, _=Depends(get_current_user)):
    repo = SecretariaRepository(db)
    return await repo.get_ativas()


@router.post("/secretarias", response_model=SecretariaResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def criar_secretaria(data: SecretariaCreate, db: DatabaseDep):
    from app.models.usuarios import Secretaria
    repo = SecretariaRepository(db)
    return await repo.create(Secretaria(**data.model_dump()))


@router.patch("/secretarias/{secretaria_id}", response_model=SecretariaResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def atualizar_secretaria(secretaria_id: int, data: SecretariaUpdate, db: DatabaseDep):
    from fastapi import HTTPException, status
    repo = SecretariaRepository(db)
    secretaria = await repo.get_by_id(secretaria_id)
    if not secretaria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Secretaria não encontrada")
    return await repo.update(secretaria, data.model_dump(exclude_none=True))


# ── Usuários ───────────────────────────────────────────────────────────────────

@router.get("", response_model=list[UsuarioResponse], dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def listar_usuarios(db: DatabaseDep, skip: int = 0, limit: int = 100):
    repo = UsuarioRepository(db)
    return await repo.get_all_with_secretaria(skip=skip, limit=limit)


@router.post("", response_model=UsuarioResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def criar_usuario(data: UsuarioCreate, db: DatabaseDep):
    service = UsuarioService(UsuarioRepository(db))
    return await service.criar(data)


@router.get("/{usuario_id}", response_model=UsuarioResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def detalhe_usuario(usuario_id: int, db: DatabaseDep):
    from fastapi import HTTPException, status
    repo = UsuarioRepository(db)
    usuario = await repo.get_with_secretaria(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def atualizar_usuario(usuario_id: int, data: UsuarioUpdate, db: DatabaseDep):
    service = UsuarioService(UsuarioRepository(db))
    return await service.atualizar(usuario_id, data)


@router.post("/me/change-password", response_model=MessageResponse)
async def alterar_senha(data: UsuarioChangePassword, db: DatabaseDep, current_user=Depends(get_current_user)):
    service = UsuarioService(UsuarioRepository(db))
    await service.alterar_senha(current_user, data)
    return MessageResponse(message="Senha alterada com sucesso")
