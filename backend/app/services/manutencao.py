from fastapi import HTTPException, status

from app.models.manutencao import SMV, SMVEtapa
from app.models.usuarios import Usuario
from app.repositories.manutencao import SMVRepository
from app.schemas.manutencao import SMVAvancarEtapa, SMVCreate, SMVUpdate

# Transições válidas do fluxo SMV
TRANSICOES_VALIDAS: dict[str, str] = {
    "SOLICITACAO": "RECEPCAO",
    "RECEPCAO": "DIAGNOSTICO",
    "DIAGNOSTICO": "ORCAMENTO",
    "ORCAMENTO": "APROVACAO",
    "APROVACAO": "EXECUCAO",
    "EXECUCAO": "RETIRADA",
    "RETIRADA": "EMISSAO_NF",
    "EMISSAO_NF": "FINALIZADO",
}

# Perfis que podem avançar cada etapa
PERFIS_POR_ETAPA: dict[str, list[str]] = {
    "RECEPCAO": ["ADMIN", "GESTOR", "OFICINA"],
    "DIAGNOSTICO": ["ADMIN", "GESTOR", "OFICINA"],
    "ORCAMENTO": ["ADMIN", "GESTOR", "OFICINA"],
    "APROVACAO": ["ADMIN", "GESTOR"],
    "EXECUCAO": ["ADMIN", "GESTOR", "OFICINA"],
    "RETIRADA": ["ADMIN", "GESTOR", "OPERADOR"],
    "EMISSAO_NF": ["ADMIN", "GESTOR"],
    "FINALIZADO": ["ADMIN", "GESTOR"],
}


class SMVService:
    def __init__(self, repo: SMVRepository) -> None:
        self.repo = repo

    async def criar(self, data: SMVCreate, solicitante: Usuario) -> SMV:
        numero = await self.repo.proximo_numero()
        smv = SMV(
            numero=numero,
            veiculo_id=data.veiculo_id,
            solicitante_id=solicitante.id,
            descricao_problema=data.descricao_problema,
            urgencia=data.urgencia,
            km_entrada=data.km_entrada,
            observacoes=data.observacoes,
        )
        return await self.repo.create(smv)

    async def get_or_404(self, smv_id: int) -> SMV:
        smv = await self.repo.get_by_id(smv_id)
        if not smv:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SMV não encontrada")
        return smv

    async def avancar_etapa(
        self, smv_id: int, data: SMVAvancarEtapa, usuario: Usuario
    ) -> SMV:
        smv = await self.get_or_404(smv_id)

        proxima = TRANSICOES_VALIDAS.get(smv.etapa)
        if proxima != data.etapa_para:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Transição inválida: {smv.etapa} → {data.etapa_para}",
            )

        perfis_permitidos = PERFIS_POR_ETAPA.get(data.etapa_para, [])
        if not usuario.is_superuser and usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Seu perfil não pode avançar para {data.etapa_para}",
            )

        historico = SMVEtapa(
            smv_id=smv.id,
            etapa_de=smv.etapa,
            etapa_para=data.etapa_para,
            responsavel_id=usuario.id,
            observacao=data.observacao,
        )
        self.repo.session.add(historico)

        from datetime import datetime, timezone
        agora = datetime.now(timezone.utc)
        campo_data = {
            "RECEPCAO": "dt_recepcao",
            "DIAGNOSTICO": "dt_diagnostico",
            "EXECUCAO": "dt_inicio_exec",
            "RETIRADA": "dt_retirada",
            "FINALIZADO": "dt_finalizacao",
        }.get(data.etapa_para)

        updates: dict = {"etapa": data.etapa_para}
        if campo_data:
            updates[campo_data] = agora

        return await self.repo.update(smv, updates)
