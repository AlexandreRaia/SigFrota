from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError

from app.core.dependencies import DatabaseDep, get_current_user, require_perfil
from app.models.veiculos import (
    Categoria,
    CentroCusto,
    Combustivel,
    Marca,
    Modelo,
    Subunidade,
    TipoFrota,
    TipoVeiculo,
    Unidade,
)
from app.repositories.veiculos import (
    CategoriaRepository,
    CentroCustoRepository,
    CombustivelRepository,
    MarcaRepository,
    ModeloRepository,
    SubunidadeRepository,
    TipoFrotaRepository,
    TipoVeiculoRepository,
    UnidadeRepository,
)
from app.schemas.common import MessageResponse
from app.schemas.veiculos import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
    CentroCustoCreate,
    CentroCustoResponse,
    CentroCustoUpdate,
    CombustivelCreate,
    CombustivelResponse,
    CombustivelUpdate,
    MarcaCreate,
    MarcaResponse,
    MarcaUpdate,
    ModeloCreate,
    ModeloResponse,
    ModeloUpdate,
    SubunidadeCreate,
    SubunidadeResponse,
    SubunidadeUpdate,
    TipoFrotaCreate,
    TipoFrotaResponse,
    TipoFrotaUpdate,
    TipoVeiculoCreate,
    TipoVeiculoResponse,
    TipoVeiculoUpdate,
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


# ── Categorias ────────────────────────────────────────────────────────────────

@router.get("/categorias", response_model=list[CategoriaResponse], dependencies=[Depends(get_current_user)])
async def listar_categorias(db: DatabaseDep):
    """Listar categorias (ativas e inativas) para gestão."""
    itens = await CategoriaRepository(db).get_all(limit=1000)
    return sorted(itens, key=lambda c: c.nome.lower())


@router.post("/categorias", response_model=CategoriaResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_categoria(data: CategoriaCreate, db: DatabaseDep):
    """Criar uma nova categoria."""
    repo = CategoriaRepository(db)
    try:
        return await repo.create(Categoria(**data.model_dump()))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe uma categoria com este nome.")


@router.patch("/categorias/{categoria_id}", response_model=CategoriaResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_categoria(categoria_id: int, data: CategoriaUpdate, db: DatabaseDep):
    """Atualizar uma categoria."""
    repo = CategoriaRepository(db)
    categoria = await repo.get_by_id(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    try:
        return await repo.update(categoria, data.model_dump(exclude_unset=True))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe uma categoria com este nome.")


@router.delete("/categorias/{categoria_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_categoria(categoria_id: int, db: DatabaseDep):
    """Excluir uma categoria."""
    repo = CategoriaRepository(db)
    categoria = await repo.get_by_id(categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    try:
        await repo.delete(categoria)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: há veículos vinculados a esta categoria. Inative-a.",
        )
    return MessageResponse(message="Categoria excluída com sucesso")


# ── Tipos de Frota ────────────────────────────────────────────────────────────

@router.get("/tipos-frota", response_model=list[TipoFrotaResponse], dependencies=[Depends(get_current_user)])
async def listar_tipos_frota(db: DatabaseDep):
    """Listar tipos de frota (ativos e inativos) para gestão."""
    itens = await TipoFrotaRepository(db).get_all(limit=1000)
    return sorted(itens, key=lambda t: t.nome.lower())


@router.post("/tipos-frota", response_model=TipoFrotaResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_tipo_frota(data: TipoFrotaCreate, db: DatabaseDep):
    """Criar um novo tipo de frota."""
    repo = TipoFrotaRepository(db)
    try:
        return await repo.create(TipoFrota(**data.model_dump()))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um tipo de frota com este nome.")


@router.patch("/tipos-frota/{tipo_frota_id}", response_model=TipoFrotaResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_tipo_frota(tipo_frota_id: int, data: TipoFrotaUpdate, db: DatabaseDep):
    """Atualizar um tipo de frota."""
    repo = TipoFrotaRepository(db)
    tipo = await repo.get_by_id(tipo_frota_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de frota não encontrado")
    try:
        return await repo.update(tipo, data.model_dump(exclude_unset=True))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um tipo de frota com este nome.")


@router.delete("/tipos-frota/{tipo_frota_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_tipo_frota(tipo_frota_id: int, db: DatabaseDep):
    """Excluir um tipo de frota."""
    repo = TipoFrotaRepository(db)
    tipo = await repo.get_by_id(tipo_frota_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de frota não encontrado")
    try:
        await repo.delete(tipo)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: há veículos vinculados a este tipo de frota. Inative-o.",
        )
    return MessageResponse(message="Tipo de frota excluído com sucesso")


# ── Tipos de Veículo ──────────────────────────────────────────────────────────

@router.get("/tipos-veiculo", response_model=list[TipoVeiculoResponse], dependencies=[Depends(get_current_user)])
async def listar_tipos_veiculo(db: DatabaseDep):
    """Listar tipos de veículo (ativos e inativos) para gestão."""
    itens = await TipoVeiculoRepository(db).get_all(limit=1000)
    return sorted(itens, key=lambda t: t.nome.lower())


@router.post("/tipos-veiculo", response_model=TipoVeiculoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_tipo_veiculo(data: TipoVeiculoCreate, db: DatabaseDep):
    """Criar um novo tipo de veículo."""
    repo = TipoVeiculoRepository(db)
    try:
        return await repo.create(TipoVeiculo(**data.model_dump()))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um tipo de veículo com este nome.")


@router.patch("/tipos-veiculo/{tipo_veiculo_id}", response_model=TipoVeiculoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_tipo_veiculo(tipo_veiculo_id: int, data: TipoVeiculoUpdate, db: DatabaseDep):
    """Atualizar um tipo de veículo."""
    repo = TipoVeiculoRepository(db)
    tipo = await repo.get_by_id(tipo_veiculo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de veículo não encontrado")
    try:
        return await repo.update(tipo, data.model_dump(exclude_unset=True))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um tipo de veículo com este nome.")


@router.delete("/tipos-veiculo/{tipo_veiculo_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_tipo_veiculo(tipo_veiculo_id: int, db: DatabaseDep):
    """Excluir um tipo de veículo."""
    repo = TipoVeiculoRepository(db)
    tipo = await repo.get_by_id(tipo_veiculo_id)
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de veículo não encontrado")
    try:
        await repo.delete(tipo)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: há veículos vinculados a este tipo de veículo. Inative-o.",
        )
    return MessageResponse(message="Tipo de veículo excluído com sucesso")


# ── Marcas ────────────────────────────────────────────────────────────────────

@router.get("/marcas", response_model=list[MarcaResponse], dependencies=[Depends(get_current_user)])
async def listar_marcas(db: DatabaseDep):
    """Listar marcas (ativas e inativas) para gestão."""
    itens = await MarcaRepository(db).get_all(limit=1000)
    return sorted(itens, key=lambda m: m.nome.lower())


@router.post("/marcas", response_model=MarcaResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_marca(data: MarcaCreate, db: DatabaseDep):
    """Criar uma nova marca."""
    repo = MarcaRepository(db)
    try:
        return await repo.create(Marca(**data.model_dump()))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe uma marca com este nome.")


@router.patch("/marcas/{marca_id}", response_model=MarcaResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_marca(marca_id: int, data: MarcaUpdate, db: DatabaseDep):
    """Atualizar uma marca."""
    repo = MarcaRepository(db)
    marca = await repo.get_by_id(marca_id)
    if not marca:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    try:
        return await repo.update(marca, data.model_dump(exclude_unset=True))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe uma marca com este nome.")


@router.delete("/marcas/{marca_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_marca(marca_id: int, db: DatabaseDep):
    """Excluir uma marca."""
    repo = MarcaRepository(db)
    marca = await repo.get_by_id(marca_id)
    if not marca:
        raise HTTPException(status_code=404, detail="Marca não encontrada")
    try:
        await repo.delete(marca)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: há modelos ou veículos vinculados a esta marca. Inative-a.",
        )
    return MessageResponse(message="Marca excluída com sucesso")


# ── Modelos ───────────────────────────────────────────────────────────────────

@router.get("/modelos", response_model=list[ModeloResponse], dependencies=[Depends(get_current_user)])
async def listar_modelos(db: DatabaseDep, marca_id: int | None = Query(None)):
    """Listar modelos (ativos e inativos) para gestão."""
    itens = await ModeloRepository(db).get_all(limit=1000)
    if marca_id is not None:
        itens = [m for m in itens if m.marca_id == marca_id]
    return sorted(itens, key=lambda m: m.nome.lower())


@router.post("/modelos", response_model=ModeloResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_modelo(data: ModeloCreate, db: DatabaseDep):
    """Criar um novo modelo."""
    repo = ModeloRepository(db)
    try:
        return await repo.create(Modelo(**data.model_dump()))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Não foi possível criar o modelo (verifique a marca informada).")


@router.patch("/modelos/{modelo_id}", response_model=ModeloResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_modelo(modelo_id: int, data: ModeloUpdate, db: DatabaseDep):
    """Atualizar um modelo."""
    repo = ModeloRepository(db)
    modelo = await repo.get_by_id(modelo_id)
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    try:
        return await repo.update(modelo, data.model_dump(exclude_unset=True))
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Não foi possível atualizar o modelo (verifique a marca informada).")


@router.delete("/modelos/{modelo_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_modelo(modelo_id: int, db: DatabaseDep):
    """Excluir um modelo."""
    repo = ModeloRepository(db)
    modelo = await repo.get_by_id(modelo_id)
    if not modelo:
        raise HTTPException(status_code=404, detail="Modelo não encontrado")
    try:
        await repo.delete(modelo)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Não é possível excluir: há veículos vinculados a este modelo. Inative-o.",
        )
    return MessageResponse(message="Modelo excluído com sucesso")


# ── Combustíveis ─────────────────────────────────────────────────────────────

@router.get("/combustiveis", response_model=list[CombustivelResponse], dependencies=[Depends(get_current_user)])
async def listar_combustiveis(db: DatabaseDep):
    """Listar todos os tipos de combustível (ativos e inativos)."""
    repo = CombustivelRepository(db)
    result = await repo.get_all()
    return sorted(result, key=lambda x: x.nome)


@router.post("/combustiveis", response_model=CombustivelResponse, status_code=201,
             dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_combustivel(data: CombustivelCreate, db: DatabaseDep):
    """Criar um novo tipo de combustível."""
    try:
        combustivel = Combustivel(nome=data.nome.strip().upper(), ativo=True)
        db.add(combustivel)
        await db.commit()
        await db.refresh(combustivel)
        return combustivel
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um combustível com este nome.")


@router.patch("/combustiveis/{combustivel_id}", response_model=CombustivelResponse,
              dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_combustivel(combustivel_id: int, data: CombustivelUpdate, db: DatabaseDep):
    """Atualizar um tipo de combustível."""
    repo = CombustivelRepository(db)
    combustivel = await repo.get_by_id(combustivel_id)
    if not combustivel:
        raise HTTPException(status_code=404, detail="Combustível não encontrado")
    try:
        if data.nome is not None:
            combustivel.nome = data.nome.strip().upper()
        if data.ativo is not None:
            combustivel.ativo = data.ativo
        await db.commit()
        await db.refresh(combustivel)
        return combustivel
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=409, detail="Já existe um combustível com este nome.")


@router.delete("/combustiveis/{combustivel_id}", response_model=MessageResponse,
               dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_combustivel(combustivel_id: int, db: DatabaseDep):
    """Excluir um tipo de combustível."""
    repo = CombustivelRepository(db)
    combustivel = await repo.get_by_id(combustivel_id)
    if not combustivel:
        raise HTTPException(status_code=404, detail="Combustível não encontrado")
    await repo.delete(combustivel)
    return MessageResponse(message="Combustível excluído com sucesso")

