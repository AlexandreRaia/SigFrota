from fastapi import HTTPException, status

from app.models.condutores import Condutor
from app.repositories.condutores import CondutorRepository
from app.schemas.condutores import CondutorCreate, CondutorUpdate


class CondutorService:
    def __init__(self, repo: CondutorRepository) -> None:
        self.repo = repo

    async def criar(self, data: CondutorCreate) -> Condutor:
        if await self.repo.get_by_cpf(data.cpf):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="CPF já cadastrado",
            )
        if await self.repo.get_by_prontuario(data.prontuario):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Prontuário já cadastrado",
            )
        condutor = Condutor(**data.model_dump())
        return await self.repo.create(condutor)

    async def atualizar(self, condutor_id: int, data: CondutorUpdate) -> Condutor:
        condutor = await self.repo.get_by_id(condutor_id)
        if not condutor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Condutor não encontrado")
        return await self.repo.update(condutor, data.model_dump(exclude_none=True))

    async def get_or_404(self, condutor_id: int) -> Condutor:
        condutor = await self.repo.get_by_id(condutor_id)
        if not condutor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Condutor não encontrado")
        return condutor
