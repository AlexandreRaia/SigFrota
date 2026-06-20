from fastapi import HTTPException, status

from app.core.security import hash_password, verify_password
from app.models.usuarios import Usuario
from app.repositories.usuarios import UsuarioRepository
from app.schemas.usuarios import UsuarioChangePassword, UsuarioCreate, UsuarioUpdate


class UsuarioService:
    def __init__(self, repo: UsuarioRepository) -> None:
        self.repo = repo

    async def criar(self, data: UsuarioCreate) -> Usuario:
        if await self.repo.get_by_username(data.username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username já em uso",
            )
        if await self.repo.get_by_email(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já em uso",
            )
        usuario = Usuario(
            username=data.username,
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            hashed_password=hash_password(data.password),
            perfil=data.perfil,
            secretaria_id=data.secretaria_id,
            telefone=data.telefone,
        )
        return await self.repo.create(usuario)

    async def atualizar(self, user_id: int, data: UsuarioUpdate) -> Usuario:
        usuario = await self.repo.get_by_id(user_id)
        if not usuario:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return await self.repo.update(usuario, data.model_dump(exclude_none=True))

    async def alterar_senha(self, usuario: Usuario, data: UsuarioChangePassword) -> None:
        if not verify_password(data.current_password, usuario.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha atual incorreta",
            )
        await self.repo.update(usuario, {"hashed_password": hash_password(data.new_password)})
