from fastapi import APIRouter

router = APIRouter(prefix="/parametrizacoes", tags=["Parametrizações"])


@router.delete("/modelos/{modelo_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_modelo(modelo_id: int, db: DatabaseDep):
    """Excluir um modelo."""
    try:
        repo = ModeloRepository(db)
        modelo = await repo.get_or_404(modelo_id)
        await repo.delete(modelo)
        return MessageResponse(message="Modelo excluído com sucesso")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── CATEGORIAS ─────────────────────────────────────────────────────────────

@router.post("/categorias", response_model=CategoriaResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def criar_categoria(
    nome: str,
    descricao: str = "",
    db: DatabaseDep
):
    """Criar uma nova categoria."""
    try:
        repo = CategoriaRepository(db)
        from app.models.veiculos import Categoria
        categoria = Categoria(nome=nome, descricao=descricao, ativa=True)
        db.add(categoria)
        await db.commit()
        await db.refresh(categoria)
        return categoria
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/categorias/{categoria_id}", response_model=CategoriaResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def atualizar_categoria(
    categoria_id: int,
    nome: str | None = None,
    descricao: str | None = None,
    ativa: bool | None = None,
    db: DatabaseDep
):
    """Atualizar uma categoria."""
    try:
        repo = CategoriaRepository(db)
        categoria = await repo.get_or_404(categoria_id)
        if nome:
            categoria.nome = nome
        if descricao is not None:
            categoria.descricao = descricao
        if ativa is not None:
            categoria.ativa = ativa
        db.add(categoria)
        await db.commit()
        await db.refresh(categoria)
        return categoria
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/categorias/{categoria_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_categoria(categoria_id: int, db: DatabaseDep):
    """Excluir uma categoria."""
    try:
        repo = CategoriaRepository(db)
        categoria = await repo.get_or_404(categoria_id)
        await repo.delete(categoria)
        return MessageResponse(message="Categoria excluída com sucesso")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── TIPOS DE FROTA ────────────────────────────────────────────────────────

@router.post("/tipos-frota", response_model=TipoFrotaResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def criar_tipo_frota(
    nome: str,
    db: DatabaseDep
):
    """Criar um novo tipo de frota."""
    try:
        from app.models.veiculos import TipoFrota
        tipo_frota = TipoFrota(nome=nome, ativa=True)
        db.add(tipo_frota)
        await db.commit()
        await db.refresh(tipo_frota)
        return tipo_frota
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/tipos-frota/{tipo_frota_id}", response_model=TipoFrotaResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def atualizar_tipo_frota(
    tipo_frota_id: int,
    nome: str | None = None,
    ativa: bool | None = None,
    db: DatabaseDep
):
    """Atualizar um tipo de frota."""
    try:
        repo = TipoFrotaRepository(db)
        tipo_frota = await repo.get_or_404(tipo_frota_id)
        if nome:
            tipo_frota.nome = nome
        if ativa is not None:
            tipo_frota.ativa = ativa
        db.add(tipo_frota)
        await db.commit()
        await db.refresh(tipo_frota)
        return tipo_frota
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/tipos-frota/{tipo_frota_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_tipo_frota(tipo_frota_id: int, db: DatabaseDep):
    """Excluir um tipo de frota."""
    try:
        repo = TipoFrotaRepository(db)
        tipo_frota = await repo.get_or_404(tipo_frota_id)
        await repo.delete(tipo_frota)
        return MessageResponse(message="Tipo de frota excluído com sucesso")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── UNIDADES ──────────────────────────────────────────────────────────────

@router.post("/unidades", response_model=UnidadeResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def criar_unidade(
    nome: str,
    secretaria_id: int,
    sigla: str = "",
    db: DatabaseDep
):
    """Criar uma nova unidade."""
    try:
        from app.models.veiculos import Unidade
        unidade = Unidade(nome=nome, secretaria_id=secretaria_id, sigla=sigla, ativa=True)
        db.add(unidade)
        await db.commit()
        await db.refresh(unidade)
        return unidade
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/unidades/{unidade_id}", response_model=UnidadeResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def atualizar_unidade(
    unidade_id: int,
    nome: str | None = None,
    sigla: str | None = None,
    ativa: bool | None = None,
    db: DatabaseDep
):
    """Atualizar uma unidade."""
    try:
        repo = UnidadeRepository(db)
        unidade = await repo.get_or_404(unidade_id)
        if nome:
            unidade.nome = nome
        if sigla is not None:
            unidade.sigla = sigla
        if ativa is not None:
            unidade.ativa = ativa
        db.add(unidade)
        await db.commit()
        await db.refresh(unidade)
        return unidade
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/unidades/{unidade_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_unidade(unidade_id: int, db: DatabaseDep):
    """Excluir uma unidade."""
    try:
        repo = UnidadeRepository(db)
        unidade = await repo.get_or_404(unidade_id)
        await repo.delete(unidade)
        return MessageResponse(message="Unidade excluída com sucesso")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── SUBUNIDADES ────────────────────────────────────────────────────────────

@router.post("/subunidades", response_model=SubunidadeResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def criar_subunidade(
    nome: str,
    unidade_id: int,
    sigla: str = "",
    db: DatabaseDep
):
    """Criar uma nova subunidade."""
    try:
        from app.models.veiculos import Subunidade
        subunidade = Subunidade(nome=nome, unidade_id=unidade_id, sigla=sigla, ativa=True)
        db.add(subunidade)
        await db.commit()
        await db.refresh(subunidade)
        return subunidade
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/subunidades/{subunidade_id}", response_model=SubunidadeResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def atualizar_subunidade(
    subunidade_id: int,
    nome: str | None = None,
    sigla: str | None = None,
    ativa: bool | None = None,
    db: DatabaseDep
):
    """Atualizar uma subunidade."""
    try:
        repo = SubunidadeRepository(db)
        subunidade = await repo.get_or_404(subunidade_id)
        if nome:
            subunidade.nome = nome
        if sigla is not None:
            subunidade.sigla = sigla
        if ativa is not None:
            subunidade.ativa = ativa
        db.add(subunidade)
        await db.commit()
        await db.refresh(subunidade)
        return subunidade
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/subunidades/{subunidade_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_subunidade(subunidade_id: int, db: DatabaseDep):
    """Excluir uma subunidade."""
    try:
        repo = SubunidadeRepository(db)
        subunidade = await repo.get_or_404(subunidade_id)
        await repo.delete(subunidade)
        return MessageResponse(message="Subunidade excluída com sucesso")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# ── CENTROS DE CUSTO ────────────────────────────────────────────────────────

@router.post("/centros-custo", response_model=CentroCustoResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def criar_centro_custo(
    codigo: str,
    nome: str,
    db: DatabaseDep
):
    """Criar um novo centro de custo."""
    try:
        from app.models.veiculos import CentroCusto
        centro_custo = CentroCusto(codigo=codigo, nome=nome, ativa=True)
        db.add(centro_custo)
        await db.commit()
        await db.refresh(centro_custo)
        return centro_custo
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.put("/centros-custo/{centro_custo_id}", response_model=CentroCustoResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def atualizar_centro_custo(
    centro_custo_id: int,
    codigo: str | None = None,
    nome: str | None = None,
    ativa: bool | None = None,
    db: DatabaseDep
):
    """Atualizar um centro de custo."""
    try:
        repo = CentroCustoRepository(db)
        centro_custo = await repo.get_or_404(centro_custo_id)
        if codigo:
            centro_custo.codigo = codigo
        if nome:
            centro_custo.nome = nome
        if ativa is not None:
            centro_custo.ativa = ativa
        db.add(centro_custo)
        await db.commit()
        await db.refresh(centro_custo)
        return centro_custo
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/centros-custo/{centro_custo_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_centro_custo(centro_custo_id: int, db: DatabaseDep):
    """Excluir um centro de custo."""
    try:
        repo = CentroCustoRepository(db)
        centro_custo = await repo.get_or_404(centro_custo_id)
        await repo.delete(centro_custo)
        return MessageResponse(message="Centro de custo excluído com sucesso")
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
