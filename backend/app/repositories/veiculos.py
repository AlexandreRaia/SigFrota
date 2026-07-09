from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.veiculos import (
    Veiculo, Marca, Modelo, TipoVeiculo, Combustivel,
    Categoria, TipoFrota, Unidade, Subunidade, CentroCusto,
    VeiculoDocumento,
)
from app.repositories.base import BaseRepository


class VeiculoRepository(BaseRepository[Veiculo]):
    """Repository para gerenciar veículos."""
    
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Veiculo, session)

    async def get_by_placa(self, placa: str) -> Veiculo | None:
        result = await self.session.execute(
            select(Veiculo).where(Veiculo.placa == placa.upper())
        )
        return result.scalar_one_or_none()

    async def get_by_prefixo(self, prefixo: str) -> Veiculo | None:
        """Buscar veículo por prefixo (deve ser único)."""
        result = await self.session.execute(
            select(Veiculo).where(Veiculo.prefixo == prefixo)
        )
        return result.scalar_one_or_none()

    async def get_com_relacoes(self, veiculo_id: int) -> Veiculo | None:
        """Buscar veículo com todas as relações carregadas."""
        result = await self.session.execute(
            select(Veiculo)
            .options(
                selectinload(Veiculo.marca),
                selectinload(Veiculo.modelo),
                selectinload(Veiculo.tipo_registro),
                selectinload(Veiculo.tipo_frota_ref),
                selectinload(Veiculo.categoria),
                selectinload(Veiculo.unidade),
                selectinload(Veiculo.subunidade),
                selectinload(Veiculo.centro_custo_ref),
            )
            .where(Veiculo.id == veiculo_id)
        )
        return result.scalar_one_or_none()

    async def listar_com_relacoes(self, skip: int = 0, limit: int = 100) -> list[Veiculo]:
        """Listar veículos com relações carregadas."""
        stmt = select(Veiculo).options(
            selectinload(Veiculo.marca),
            selectinload(Veiculo.modelo),
            selectinload(Veiculo.tipo_registro),
            selectinload(Veiculo.categoria),
        ).offset(skip).limit(limit).order_by(Veiculo.placa)
        
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def pesquisar(
        self,
        q: str = "",
        situacao: str = "",
        categoria_id: int | None = None,
        tipo_frota_id: int | None = None,
        secretaria_id: int | None = None,
        unidade_id: int | None = None,
        centro_custo_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Veiculo]:
        """Pesquisar veículos com filtros múltiplos."""
        stmt = select(Veiculo).options(
            selectinload(Veiculo.marca),
            selectinload(Veiculo.modelo),
            selectinload(Veiculo.categoria),
            selectinload(Veiculo.unidade),
        )
        
        filters = []
        
        if q:
            filters.append(
                or_(
                    Veiculo.placa.ilike(f"%{q}%"),
                    Veiculo.prefixo.ilike(f"%{q}%"),
                    Veiculo.chassi.ilike(f"%{q}%"),
                    Veiculo.renavam.ilike(f"%{q}%"),
                )
            )
        if situacao:
            filters.append(Veiculo.situacao == situacao)
        if categoria_id:
            filters.append(Veiculo.categoria_id == categoria_id)
        if tipo_frota_id:
            filters.append(Veiculo.tipo_frota_id == tipo_frota_id)
        if secretaria_id:
            filters.append(Veiculo.secretaria_id == secretaria_id)
        if unidade_id:
            filters.append(Veiculo.unidade_id == unidade_id)
        if centro_custo_id:
            filters.append(Veiculo.centro_custo_id == centro_custo_id)

        if filters:
            stmt = stmt.where(and_(*filters))

        stmt = stmt.offset(skip).limit(limit).order_by(Veiculo.placa)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())


# ── Repositórios Parametrizadores ──────────────────────────────────────────

class CategoriaRepository(BaseRepository[Categoria]):
    """Repository para Categorias de veículos."""
    
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Categoria, session)

    async def get_ativas(self) -> list[Categoria]:
        result = await self.session.execute(
            select(Categoria).where(Categoria.ativa == True).order_by(Categoria.nome)
        )
        return list(result.scalars().all())


class TipoFrotaRepository(BaseRepository[TipoFrota]):
    """Repository para Tipos de Frota."""
    
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(TipoFrota, session)

    async def get_ativos(self) -> list[TipoFrota]:
        result = await self.session.execute(
            select(TipoFrota).where(TipoFrota.ativa == True).order_by(TipoFrota.nome)
        )
        return list(result.scalars().all())


class UnidadeRepository(BaseRepository[Unidade]):
    """Repository para Unidades administrativas."""
    
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Unidade, session)

    async def get_ativas(self) -> list[Unidade]:
        result = await self.session.execute(
            select(Unidade).where(Unidade.ativa == True).order_by(Unidade.nome)
        )
        return list(result.scalars().all())

    async def get_por_secretaria(self, secretaria_id: int) -> list[Unidade]:
        """Buscar unidades de uma secretaria."""
        result = await self.session.execute(
            select(Unidade)
            .where(and_(
                Unidade.secretaria_id == secretaria_id,
                Unidade.ativa == True
            ))
            .order_by(Unidade.nome)
        )
        return list(result.scalars().all())


class SubunidadeRepository(BaseRepository[Subunidade]):
    """Repository para Subunidades administrativas."""
    
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Subunidade, session)

    async def get_ativas(self) -> list[Subunidade]:
        result = await self.session.execute(
            select(Subunidade).where(Subunidade.ativa == True).order_by(Subunidade.nome)
        )
        return list(result.scalars().all())

    async def get_por_unidade(self, unidade_id: int) -> list[Subunidade]:
        """Buscar subunidades de uma unidade."""
        result = await self.session.execute(
            select(Subunidade)
            .where(and_(
                Subunidade.unidade_id == unidade_id,
                Subunidade.ativa == True
            ))
            .order_by(Subunidade.nome)
        )
        return list(result.scalars().all())


class CentroCustoRepository(BaseRepository[CentroCusto]):
    """Repository para Centros de Custo."""
    
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(CentroCusto, session)

    async def get_ativos(self) -> list[CentroCusto]:
        result = await self.session.execute(
            select(CentroCusto).where(CentroCusto.ativa == True).order_by(CentroCusto.codigo)
        )
        return list(result.scalars().all())


# ── Repositórios Base (Marca, Modelo, TipoVeiculo) ────────────────────────

class MarcaRepository(BaseRepository[Marca]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Marca, session)

    async def get_ativas(self) -> list[Marca]:
        result = await self.session.execute(
            select(Marca).where(Marca.ativo == True).order_by(Marca.nome)
        )
        return list(result.scalars().all())


class ModeloRepository(BaseRepository[Modelo]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Modelo, session)

    async def get_por_marca(self, marca_id: int) -> list[Modelo]:
        result = await self.session.execute(
            select(Modelo)
            .where(and_(Modelo.marca_id == marca_id, Modelo.ativo == True))
            .order_by(Modelo.nome)
        )
        return list(result.scalars().all())


class TipoVeiculoRepository(BaseRepository[TipoVeiculo]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(TipoVeiculo, session)

    async def get_ativos(self) -> list[TipoVeiculo]:
        result = await self.session.execute(
            select(TipoVeiculo).where(TipoVeiculo.ativo == True).order_by(TipoVeiculo.nome)
        )
        return list(result.scalars().all())


class CombustivelRepository(BaseRepository[Combustivel]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(Combustivel, session)

    async def get_ativos(self) -> list[Combustivel]:
        result = await self.session.execute(
            select(Combustivel).where(Combustivel.ativo == True).order_by(Combustivel.nome)
        )
        return list(result.scalars().all())


class DocumentoRepository(BaseRepository[VeiculoDocumento]):
    """Repository para documentos e fotos vinculados a veículos."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(VeiculoDocumento, session)

    async def listar_por_veiculo(self, veiculo_id: int) -> list[VeiculoDocumento]:
        result = await self.session.execute(
            select(VeiculoDocumento)
            .where(VeiculoDocumento.veiculo_id == veiculo_id)
            .order_by(VeiculoDocumento.criado_em.desc())
        )
        return list(result.scalars().all())
