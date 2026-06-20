from fastapi import HTTPException, status

from app.models.veiculos import Veiculo
from app.repositories.veiculos import VeiculoRepository
from app.schemas.veiculos import VeiculoCreate, VeiculoUpdate


class VeiculoService:
    """Service para operações de negócio com veículos."""
    
    def __init__(self, repo: VeiculoRepository) -> None:
        self.repo = repo

    async def criar(self, data: VeiculoCreate) -> Veiculo:
        """Criar novo veículo com validações."""
        
        # Validar PLACA (obrigatória, única)
        placa = (data.placa or '').upper()
        if not placa or len(placa) < 7:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Placa inválida (mínimo 7 caracteres)"
            )
        if await self.repo.get_by_placa(placa):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Veículo com placa {placa} já cadastrado"
            )
        
        # Validar PREFIXO (obrigatório, único)
        prefixo = (data.prefixo or '').strip()
        if not prefixo:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Prefixo é obrigatório"
            )
        if await self.repo.get_by_prefixo(prefixo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Prefixo {prefixo} já utilizado"
            )
        
        # Validar CHASSI (17 caracteres)
        chassi = (data.chassi or '').strip().upper()
        if len(chassi) != 17:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Chassi deve ter exatamente 17 caracteres"
            )
        
        # Validar RENAVAM (11 dígitos numéricos)
        renavam = (data.renavam or '').strip()
        if not renavam.isdigit() or len(renavam) != 11:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="RENAVAM deve ter exatamente 11 dígitos"
            )
        
        # Validar relações obrigatórias
        if not data.marca_id or not data.modelo_id:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Marca e Modelo são obrigatórios"
            )
        
        # Criar veículo
        dump = data.model_dump()
        dump['placa'] = placa
        dump['chassi'] = chassi
        
        veiculo = Veiculo(**dump)
        veiculo = await self.repo.create(veiculo)
        
        return await self.get_or_404(veiculo.id)

    async def atualizar(self, veiculo_id: int, data: VeiculoUpdate) -> Veiculo:
        """Atualizar veículo com validações."""
        veiculo = await self.repo.get_by_id(veiculo_id)
        if not veiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veículo não encontrado"
            )
        
        # Validar PREFIXO se fornecido
        if data.prefixo is not None:
            prefixo = data.prefixo.strip()
            if not prefixo:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Prefixo não pode estar vazio"
                )
            # Verificar se prefixo já existe (em outro veículo)
            existing = await self.repo.get_by_prefixo(prefixo)
            if existing and existing.id != veiculo_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Prefixo {prefixo} já utilizado por outro veículo"
                )
        
        # Atualizar
        await self.repo.update(veiculo, data.model_dump(exclude_none=True))
        return await self.get_or_404(veiculo_id)

    async def get_or_404(self, veiculo_id: int) -> Veiculo:
        """Buscar veículo com todas as relações ou retornar 404."""
        veiculo = await self.repo.get_com_relacoes(veiculo_id)
        if not veiculo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Veículo não encontrado"
            )
        return veiculo
