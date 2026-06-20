from fastapi import HTTPException, status

from app.core.security import create_access_token, create_refresh_token, decode_token, verify_password
from app.repositories.usuarios import UsuarioRepository
from app.schemas.auth import AccessTokenResponse, TokenResponse


class AuthService:
    def __init__(self, repo: UsuarioRepository) -> None:
        self.repo = repo

    async def login(self, username: str, password: str) -> TokenResponse:
        user = await self.repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas",
            )
        if not user.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo",
            )
        extra = {"perfil": user.perfil, "username": user.username}
        return TokenResponse(
            access_token=create_access_token(user.id, extra),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh(self, refresh_token: str) -> AccessTokenResponse:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido ou expirado",
            )
        user_id = payload.get("sub")
        user = await self.repo.get_by_id(int(user_id))
        if not user or not user.ativo:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não encontrado ou inativo",
            )
        extra = {"perfil": user.perfil, "username": user.username}
        return AccessTokenResponse(
            access_token=create_access_token(user.id, extra),
        )
