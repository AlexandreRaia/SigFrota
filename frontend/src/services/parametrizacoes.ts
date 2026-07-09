import api from './api'
import type { Unidade, Subunidade, CentroCusto } from '@/types'

export interface UnidadePayload {
  nome: string
  sigla?: string
  secretaria_id?: number | null
  ativa?: boolean
}

export interface SubunidadePayload {
  nome: string
  unidade_id: number
  sigla?: string
  ativa?: boolean
}

export interface CentroCustoPayload {
  codigo: string
  nome: string
  ativa?: boolean
}

export const parametrizacaoService = {
  // ── Unidades ────────────────────────────────────────────────────────────────

  async listarUnidades(secretariaId?: number): Promise<Unidade[]> {
    const params = secretariaId ? { secretaria_id: secretariaId } : undefined
    const response = await api.get<Unidade[]>('/parametrizacoes/unidades', { params })
    return response.data
  },

  async criarUnidade(data: UnidadePayload): Promise<Unidade> {
    const response = await api.post<Unidade>('/parametrizacoes/unidades', data)
    return response.data
  },

  async atualizarUnidade(id: number, data: Partial<UnidadePayload>): Promise<Unidade> {
    const response = await api.patch<Unidade>(`/parametrizacoes/unidades/${id}`, data)
    return response.data
  },

  async excluirUnidade(id: number): Promise<void> {
    await api.delete(`/parametrizacoes/unidades/${id}`)
  },

  // ── Subunidades ─────────────────────────────────────────────────────────────

  async listarSubunidades(unidadeId?: number): Promise<Subunidade[]> {
    const params = unidadeId ? { unidade_id: unidadeId } : undefined
    const response = await api.get<Subunidade[]>('/parametrizacoes/subunidades', { params })
    return response.data
  },

  async criarSubunidade(data: SubunidadePayload): Promise<Subunidade> {
    const response = await api.post<Subunidade>('/parametrizacoes/subunidades', data)
    return response.data
  },

  async atualizarSubunidade(id: number, data: Partial<SubunidadePayload>): Promise<Subunidade> {
    const response = await api.patch<Subunidade>(`/parametrizacoes/subunidades/${id}`, data)
    return response.data
  },

  async excluirSubunidade(id: number): Promise<void> {
    await api.delete(`/parametrizacoes/subunidades/${id}`)
  },

  // ── Centros de Custo ───────────────────────────────────────────────────

  async listarCentrosCusto(): Promise<CentroCusto[]> {
    const response = await api.get<CentroCusto[]>('/parametrizacoes/centros-custo')
    return response.data
  },

  async criarCentroCusto(data: CentroCustoPayload): Promise<CentroCusto> {
    const response = await api.post<CentroCusto>('/parametrizacoes/centros-custo', data)
    return response.data
  },

  async atualizarCentroCusto(id: number, data: Partial<CentroCustoPayload>): Promise<CentroCusto> {
    const response = await api.patch<CentroCusto>(`/parametrizacoes/centros-custo/${id}`, data)
    return response.data
  },

  async excluirCentroCusto(id: number): Promise<void> {
    await api.delete(`/parametrizacoes/centros-custo/${id}`)
  },
}
