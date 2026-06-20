from fastapi import HTTPException, status

from app.models.multas import Multa
from app.repositories.multas import MultaRepository
from app.schemas.multas import MultaCreate, MultaUpdate


class MultaService:
    def __init__(self, repo: MultaRepository) -> None:
        self.repo = repo

    async def criar(self, data: MultaCreate) -> Multa:
        multa = Multa(**data.model_dump())
        multa.placa = multa.placa.upper()
        return await self.repo.create(multa)

    async def atualizar(self, multa_id: int, data: MultaUpdate) -> Multa:
        multa = await self.repo.get_by_id(multa_id)
        if not multa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Multa não encontrada")
        return await self.repo.update(multa, data.model_dump(exclude_none=True))

    async def get_or_404(self, multa_id: int) -> Multa:
        multa = await self.repo.get_by_id(multa_id)
        if not multa:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Multa não encontrada")
        return multa
