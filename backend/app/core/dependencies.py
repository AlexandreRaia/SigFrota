from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal
from app.core.security import decode_token

bearer_scheme = HTTPBearer()


async def get_db() -> AsyncSession:  # type: ignore[misc]
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: DatabaseDep,
):
    from app.repositories.usuarios import UsuarioRepository

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise credentials_exception

    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    repo = UsuarioRepository(db)
    # usa método que faz eager-load da relação `secretaria` para evitar
    # acesso lazy que dispararia IO fora do contexto async.
    user = await repo.get_with_secretaria(int(user_id))
    if not user or not user.ativo:
        raise credentials_exception

    return user


CurrentUserDep = Annotated[object, Depends(get_current_user)]


def require_perfil(*perfis: str):
    """Dependência que restringe o acesso a perfis específicos."""

    async def checker(current_user=Depends(get_current_user)):
        if current_user.is_superuser:
            return current_user
        if current_user.perfil not in perfis:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acesso restrito. Perfis permitidos: {', '.join(perfis)}",
            )
        return current_user

    return checker
