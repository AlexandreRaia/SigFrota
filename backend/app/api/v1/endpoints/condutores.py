import re
import uuid
from pathlib import Path

import aiofiles
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile

from app.core.config import settings
from app.core.dependencies import DatabaseDep, get_current_user, require_perfil
from app.models.condutores import CondutorDocumento
from app.repositories.condutores import CondutorRepository, CondutorDocumentoRepository
from app.repositories.veiculos import UnidadeRepository, SubunidadeRepository
from app.schemas.common import MessageResponse
from app.schemas.condutores import (
    CondutorCreate, CondutorListItem, CondutorResponse, CondutorUpdate,
    CondutorDocumentoResponse,
)
from app.schemas.veiculos import UnidadeResponse, SubunidadeResponse
from app.services.condutores import CondutorService

router = APIRouter(prefix="/condutores", tags=["Condutores"])

_TIPOS_VALIDOS = {"FOTO", "CNH", "OUTRO"}
_EXTENSOES_VALIDAS = {".jpg", ".jpeg", ".png", ".pdf", ".webp"}
_TAMANHO_MAX_BYTES = 10 * 1024 * 1024  # 10 MB


def _nome_para_pasta(nome: str) -> str:
    """Sanitiza o nome do condutor para usar como nome de pasta."""
    return re.sub(r'[^A-Z0-9]', '-', nome.upper())[:40]


# ── Lookups de Parametrização ────────────────────────────────────────────────────────

@router.get("/parametrizacoes/unidades", response_model=list[UnidadeResponse], dependencies=[Depends(get_current_user)])
async def listar_unidades(db: DatabaseDep):
    """Listar unidades ativas para seleção no formulário."""
    return await UnidadeRepository(db).get_ativas()


@router.get("/parametrizacoes/subunidades", response_model=list[SubunidadeResponse], dependencies=[Depends(get_current_user)])
async def listar_subunidades(db: DatabaseDep, unidade_id: int | None = Query(None)):
    """Listar subunidades ativas para seleção no formulário."""
    repo = SubunidadeRepository(db)
    if unidade_id:
        return await repo.get_por_unidade(unidade_id)
    return await repo.get_ativas()


# ── CRUD de Condutores ─────────────────────────────────────────────────────────

@router.get("", response_model=list[CondutorListItem], dependencies=[Depends(get_current_user)])
async def listar_condutores(
    db: DatabaseDep,
    q: str = Query(""),
    status: str = Query(""),
    unidade_id: int | None = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    return await CondutorRepository(db).search(q=q, status=status, unidade_id=unidade_id, skip=skip, limit=limit)


@router.post("", response_model=CondutorResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def criar_condutor(data: CondutorCreate, db: DatabaseDep):
    service = CondutorService(CondutorRepository(db))
    condutor = await service.criar(data)
    return await CondutorRepository(db).get_com_relacoes(condutor.id)


@router.get("/{condutor_id}", response_model=CondutorResponse, dependencies=[Depends(get_current_user)])
async def detalhe_condutor(condutor_id: int, db: DatabaseDep):
    condutor = await CondutorRepository(db).get_com_relacoes(condutor_id)
    if not condutor:
        raise HTTPException(status_code=404, detail="Condutor não encontrado")
    return condutor


@router.patch("/{condutor_id}", response_model=CondutorResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def atualizar_condutor(condutor_id: int, data: CondutorUpdate, db: DatabaseDep):
    service = CondutorService(CondutorRepository(db))
    await service.atualizar(condutor_id, data)
    return await CondutorRepository(db).get_com_relacoes(condutor_id)


@router.patch("/{condutor_id}/ativar", response_model=CondutorResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def ativar_condutor(condutor_id: int, db: DatabaseDep):
    repo = CondutorRepository(db)
    condutor = await repo.get_by_id(condutor_id)
    if not condutor:
        raise HTTPException(status_code=404, detail="Condutor não encontrado")
    await repo.update(condutor, {"status": "ATIVO"})
    return await repo.get_com_relacoes(condutor_id)


@router.patch("/{condutor_id}/inativar", response_model=CondutorResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def inativar_condutor(condutor_id: int, db: DatabaseDep):
    repo = CondutorRepository(db)
    condutor = await repo.get_by_id(condutor_id)
    if not condutor:
        raise HTTPException(status_code=404, detail="Condutor não encontrado")
    await repo.update(condutor, {"status": "INATIVO"})
    return await repo.get_com_relacoes(condutor_id)


@router.delete("/{condutor_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN"))])
async def excluir_condutor(condutor_id: int, db: DatabaseDep):
    service = CondutorService(CondutorRepository(db))
    condutor = await service.get_or_404(condutor_id)
    await CondutorRepository(db).delete(condutor)
    return MessageResponse(message="Condutor excluído com sucesso")


# ── Documentos do Condutor ────────────────────────────────────────────────────

@router.get("/{condutor_id}/documentos", response_model=list[CondutorDocumentoResponse], dependencies=[Depends(get_current_user)])
async def listar_documentos(condutor_id: int, db: DatabaseDep):
    """Listar todos os documentos de um condutor."""
    condutor = await CondutorRepository(db).get_by_id(condutor_id)
    if not condutor:
        raise HTTPException(status_code=404, detail="Condutor não encontrado")
    return await CondutorDocumentoRepository(db).listar_por_condutor(condutor_id)


@router.post("/{condutor_id}/documentos", response_model=CondutorDocumentoResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def upload_documento(
    condutor_id: int,
    db: DatabaseDep,
    tipo: str = Form(...),
    descricao: str = Form(""),
    arquivo: UploadFile = File(...),
):
    """Upload de documento para um condutor. Salvo em media/condutores/{id}/{tipo}/."""
    condutor = await CondutorRepository(db).get_by_id(condutor_id)
    if not condutor:
        raise HTTPException(status_code=404, detail="Condutor não encontrado")

    tipo = tipo.upper()
    if tipo not in _TIPOS_VALIDOS:
        raise HTTPException(status_code=400, detail=f"Tipo inválido. Permitidos: {', '.join(sorted(_TIPOS_VALIDOS))}")

    ext = Path(arquivo.filename or "").suffix.lower()
    if ext not in _EXTENSOES_VALIDAS:
        raise HTTPException(status_code=400, detail="Formato não permitido. Use: JPG, PNG, PDF ou WEBP")

    conteudo = await arquivo.read()
    if len(conteudo) > _TAMANHO_MAX_BYTES:
        raise HTTPException(status_code=400, detail="Arquivo muito grande. Máximo: 10 MB")

    pasta = _nome_para_pasta(condutor.nome)
    nome_arquivo = f"{uuid.uuid4().hex}{ext}"
    caminho_relativo = f"condutores/{pasta}/{tipo}/{nome_arquivo}"
    caminho_absoluto = Path(settings.MEDIA_DIR) / caminho_relativo

    caminho_absoluto.parent.mkdir(parents=True, exist_ok=True)
    async with aiofiles.open(caminho_absoluto, "wb") as f:
        await f.write(conteudo)

    doc = CondutorDocumento(
        condutor_id=condutor_id,
        tipo=tipo,
        descricao=descricao.strip()[:200],
        arquivo=caminho_relativo,
    )
    return await CondutorDocumentoRepository(db).create(doc)


@router.delete("/{condutor_id}/documentos/{doc_id}", response_model=MessageResponse, dependencies=[Depends(require_perfil("ADMIN", "GESTOR"))])
async def deletar_documento(condutor_id: int, doc_id: int, db: DatabaseDep):
    """Remover documento de um condutor (arquivo físico + registro no banco)."""
    repo = CondutorDocumentoRepository(db)
    doc = await repo.get_by_id(doc_id)
    if not doc or doc.condutor_id != condutor_id:
        raise HTTPException(status_code=404, detail="Documento não encontrado")

    caminho = Path(settings.MEDIA_DIR) / doc.arquivo
    if caminho.exists():
        caminho.unlink()

    await repo.delete(doc)
    return MessageResponse(message="Documento removido com sucesso")
