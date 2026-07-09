import re
import uuid
from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
import traceback

from app.core.config import settings
from app.core.dependencies import DatabaseDep, get_current_user, require_perfil
from app.models.veiculos import VeiculoDocumento
from app.repositories.veiculos import (
    VeiculoRepository, MarcaRepository, ModeloRepository, TipoVeiculoRepository,
    CategoriaRepository, TipoFrotaRepository, UnidadeRepository,
    SubunidadeRepository, CentroCustoRepository, CombustivelRepository,
    DocumentoRepository,
)
from app.schemas.common import MessageResponse
from app.schemas.veiculos import (
    MarcaResponse, ModeloResponse, TipoVeiculoResponse,
    CategoriaResponse, TipoFrotaResponse, UnidadeResponse,
    SubunidadeResponse, CentroCustoResponse, CombustivelResponse,
    VeiculoCreate, VeiculoListItem, VeiculoResponse, VeiculoUpdate,
    DocumentoResponse,
)
from app.services.veiculos import VeiculoService

router = APIRouter(prefix="/veiculos", tags=["Veículos"])

# Constantes de upload
_TIPOS_VALIDOS = {"FOTO", "CRLV", "NF_COMPRA", "APOLICE_SEGURO", "MANUTENCAO", "INSPECAO", "OUTRO"}
_EXTENSOES_VALIDAS = {".jpg", ".jpeg", ".png", ".pdf", ".webp"}
_TAMANHO_MAX_BYTES = 10 * 1024 * 1024  # 10 MB


def _placa_para_pasta(placa: str) -> str:
    """Sanitiza a placa para usar como nome de pasta."""
    return re.sub(r'[^A-Z0-9]', '-', placa.upper())


# ── Lookups Parametrizadores ───────────────────────────────────────────────

@router.get("/parametrizacoes/categorias", response_model=list[CategoriaResponse], dependencies=[Depends(get_current_user)])
async def listar_categorias(db: DatabaseDep):
    """Listar todas as categorias de veículos."""
    return await CategoriaRepository(db).get_ativas()


@router.get("/parametrizacoes/tipos-frota", response_model=list[TipoFrotaResponse], dependencies=[Depends(get_current_user)])
async def listar_tipos_frota(db: DatabaseDep):
    """Listar todos os tipos de frota."""
    return await TipoFrotaRepository(db).get_ativos()


@router.get("/parametrizacoes/unidades", response_model=list[UnidadeResponse], dependencies=[Depends(get_current_user)])
async def listar_unidades(db: DatabaseDep, secretaria_id: int | None = Query(None)):
    """Listar unidades administrativas."""
    repo = UnidadeRepository(db)
    if secretaria_id:
        return await repo.get_por_secretaria(secretaria_id)
    return await repo.get_ativas()


@router.get("/parametrizacoes/subunidades", response_model=list[SubunidadeResponse], dependencies=[Depends(get_current_user)])
async def listar_subunidades(db: DatabaseDep, unidade_id: int | None = Query(None)):
    """Listar subunidades administrativas."""
    repo = SubunidadeRepository(db)
    if unidade_id:
        return await repo.get_por_unidade(unidade_id)
    return await repo.get_ativas()


@router.get("/parametrizacoes/centros-custo", response_model=list[CentroCustoResponse], dependencies=[Depends(get_current_user)])
async def listar_centros_custo(db: DatabaseDep):
    """Listar todos os centros de custo."""
    return await CentroCustoRepository(db).get_ativos()

@router.get("/parametrizacoes/combustiveis", response_model=list[CombustivelResponse], dependencies=[Depends(get_current_user)])
async def listar_combustiveis(db: DatabaseDep):
    """Listar tipos de combustível ativos."""
    return await CombustivelRepository(db).get_ativos()

# ── Lookups Base (Marca, Modelo, TipoVeiculo) ───────────────────────────────

@router.get("/tipos-veiculo", response_model=list[TipoVeiculoResponse], dependencies=[Depends(get_current_user)])
async def listar_tipos_veiculo(db: DatabaseDep):
    """Listar tipos de registro (VEICULO, MAQUINA, EQUIPAMENTO)."""
    return await TipoVeiculoRepository(db).get_ativos()


@router.get("/marcas", response_model=list[MarcaResponse], dependencies=[Depends(get_current_user)])
async def listar_marcas(db: DatabaseDep):
    """Listar todas as marcas de veículos."""
    return await MarcaRepository(db).get_ativas()


@router.get("/modelos", response_model=list[ModeloResponse], dependencies=[Depends(get_current_user)])
async def listar_modelos(marca_id: int, db: DatabaseDep):
    """Listar modelos de uma marca específica."""
    return await ModeloRepository(db).get_por_marca(marca_id)


# ── Veículos ───────────────────────────────────────────────────────────────────

@router.get("", response_model=list[VeiculoListItem], dependencies=[Depends(get_current_user)])
async def listar_veiculos(
    db: DatabaseDep,
    q: str = Query("", description="Busca por placa, prefixo, chassi ou RENAVAM"),
    situacao: str = Query(""),
    categoria_id: int | None = Query(None),
    tipo_frota_id: int | None = Query(None),
    secretaria_id: int | None = Query(None),
    unidade_id: int | None = Query(None),
    centro_custo_id: int | None = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    """Listar veículos com filtros opcionais."""
    repo = VeiculoRepository(db)
    return await repo.pesquisar(
        q=q,
        situacao=situacao,
        categoria_id=categoria_id,
        tipo_frota_id=tipo_frota_id,
        secretaria_id=secretaria_id,
        unidade_id=unidade_id,
        centro_custo_id=centro_custo_id,
        skip=skip,
        limit=limit
    )


@router.post("", response_model=VeiculoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_veiculo(data: VeiculoCreate, db: DatabaseDep):
    """Criar um novo veículo."""
    service = VeiculoService(VeiculoRepository(db))
    try:
        return await service.criar(data)
    except HTTPException:
        raise
    except Exception as exc:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{veiculo_id}", response_model=VeiculoResponse, dependencies=[Depends(get_current_user)])
async def detalhe_veiculo(veiculo_id: int, db: DatabaseDep):
    """Obter detalhes de um veículo específico."""
    service = VeiculoService(VeiculoRepository(db))
    return await service.get_or_404(veiculo_id)


@router.patch("/{veiculo_id}", response_model=VeiculoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_veiculo(veiculo_id: int, data: VeiculoUpdate, db: DatabaseDep):
    """Atualizar informações de um veículo."""
    service = VeiculoService(VeiculoRepository(db))
    return await service.atualizar(veiculo_id, data)


@router.post("/{veiculo_id}/ativar", response_model=VeiculoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def ativar_veiculo(veiculo_id: int, db: DatabaseDep):
    """Ativar um veículo (mudar situação para ATIVA)."""
    repo = VeiculoRepository(db)
    veiculo = await repo.get_by_id(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    await repo.update(veiculo, {"situacao": "ATIVA"})
    return await repo.get_com_relacoes(veiculo_id)


@router.post("/{veiculo_id}/inativar", response_model=VeiculoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def inativar_veiculo(veiculo_id: int, db: DatabaseDep):
    """Inativar um veículo (mudar situação para INATIVA)."""
    repo = VeiculoRepository(db)
    veiculo = await repo.get_by_id(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    await repo.update(veiculo, {"situacao": "INATIVA"})
    return await repo.get_com_relacoes(veiculo_id)


@router.delete("/{veiculo_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_veiculo(veiculo_id: int, db: DatabaseDep):
    """Excluir um veículo."""
    repo = VeiculoRepository(db)
    veiculo = await repo.get_by_id(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    await repo.delete(veiculo)
    return MessageResponse(message="Veículo excluído com sucesso")


# ── Documentos do Veículo ─────────────────────────────────────────────────────

@router.get("/{veiculo_id}/documentos", response_model=list[DocumentoResponse], dependencies=[Depends(get_current_user)])
async def listar_documentos(veiculo_id: int, db: DatabaseDep):
    """Listar todos os documentos/arquivos de um veículo."""
    veiculo = await VeiculoRepository(db).get_by_id(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return await DocumentoRepository(db).listar_por_veiculo(veiculo_id)


@router.post("/{veiculo_id}/documentos", response_model=DocumentoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def upload_documento(
    veiculo_id: int,
    db: DatabaseDep,
    tipo: str = Form(...),
    descricao: str = Form(""),
    arquivo: UploadFile = File(...),
):
    """Fazer upload de um documento para um veículo. Arquivo salvo em media/veiculos/{placa}/{tipo}/."""
    veiculo = await VeiculoRepository(db).get_by_id(veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    tipo = tipo.upper()
    if tipo not in _TIPOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Tipo inválido. Permitidos: {', '.join(sorted(_TIPOS_VALIDOS))}")

    ext = Path(arquivo.filename or "").suffix.lower()
    if ext not in _EXTENSOES_VALIDAS:
        raise HTTPException(status_code=400, detail="Formato não permitido. Use: JPG, PNG, PDF ou WEBP")

    conteudo = await arquivo.read()
    if len(conteudo) > _TAMANHO_MAX_BYTES:
        raise HTTPException(status_code=400, detail="Arquivo muito grande. Máximo permitido: 10 MB")

    placa_dir = _placa_para_pasta(veiculo.placa)
    nome_arquivo = f"{uuid.uuid4().hex}{ext}"
    caminho_relativo = f"veiculos/{placa_dir}/{tipo}/{nome_arquivo}"
    caminho_absoluto = Path(settings.MEDIA_DIR) / caminho_relativo

    caminho_absoluto.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(caminho_absoluto, "wb") as f:
        await f.write(conteudo)

    doc = VeiculoDocumento(
        veiculo_id=veiculo_id,
        tipo=tipo,
        descricao=descricao.strip()[:200],
        arquivo=caminho_relativo,
    )
    return await DocumentoRepository(db).create(doc)


@router.delete("/{veiculo_id}/documentos/{doc_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def deletar_documento(veiculo_id: int, doc_id: int, db: DatabaseDep):
    """Remover um documento de um veículo (arquivo físico + registro no banco)."""
    repo = DocumentoRepository(db)
    doc = await repo.get_by_id(doc_id)
    if not doc or doc.veiculo_id != veiculo_id:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    caminho = Path(settings.MEDIA_DIR) / doc.arquivo
    if caminho.exists():
        caminho.unlink()

    await repo.delete(doc)
    return MessageResponse(message="Documento removido com sucesso")

