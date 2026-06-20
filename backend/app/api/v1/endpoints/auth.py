from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import DatabaseDep, get_current_user
from app.repositories.usuarios import UsuarioRepository
from app.schemas.auth import AccessTokenResponse, LoginRequest, RefreshRequest, TokenResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: DatabaseDep):
    service = AuthService(UsuarioRepository(db))
    return await service.login(data.username, data.password)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh_token(data: RefreshRequest, db: DatabaseDep):
    service = AuthService(UsuarioRepository(db))
    return await service.refresh(data.refresh_token)


@router.get("/me")
async def me(current_user=Depends(get_current_user)):
    from app.schemas.usuarios import UsuarioMe
    return UsuarioMe.model_validate(current_user)
