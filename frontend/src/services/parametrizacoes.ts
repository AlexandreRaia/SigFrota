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

// ── Lookups simples (nome + ativo) ────────────────────────────────────────────

export interface LookupItem {
  id: number
  nome: string
  ativo: boolean
}

export interface CategoriaItem extends LookupItem {
  descricao: string
}

export interface ModeloItem extends LookupItem {
  marca_id: number
}

export interface LookupPayload {
  nome?: string
  ativo?: boolean
}

export interface CategoriaLookupPayload extends LookupPayload {
  descricao?: string
}

export interface ModeloPayload extends LookupPayload {
  marca_id?: number
}

/** Converte o payload do frontend (ativo) para o campo do backend (ativa). */
function toAtivaPayload(data: LookupPayload & { descricao?: string; marca_id?: number }) {
  const payload: Record<string, unknown> = {}
  if (data.nome !== undefined) payload.nome = data.nome
  if (data.descricao !== undefined) payload.descricao = data.descricao
  if (data.marca_id !== undefined) payload.marca_id = data.marca_id
  if (data.ativo !== undefined) payload.ativa = data.ativo
  return payload
}

/** Converte o payload do frontend (ativo) mantendo o campo do backend (ativo). */
function toAtivoPayload(data: LookupPayload & { marca_id?: number }) {
  const payload: Record<string, unknown> = {}
  if (data.nome !== undefined) payload.nome = data.nome
  if (data.marca_id !== undefined) payload.marca_id = data.marca_id
  if (data.ativo !== undefined) payload.ativo = data.ativo
  return payload
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

  // ── Tipos de Frota ────────────────────────────────────────────────────────
  async listarTiposFrota(): Promise<LookupItem[]> {
    const { data } = await api.get<any[]>('/parametrizacoes/tipos-frota')
    return data.map((x) => ({ id: x.id, nome: x.nome, ativo: x.ativa }))
  },
  async criarTipoFrota(data: LookupPayload): Promise<void> {
    await api.post('/parametrizacoes/tipos-frota', toAtivaPayload(data))
  },
  async atualizarTipoFrota(id: number, data: LookupPayload): Promise<void> {
    await api.patch(`/parametrizacoes/tipos-frota/${id}`, toAtivaPayload(data))
  },
  async excluirTipoFrota(id: number): Promise<void> {
    await api.delete(`/parametrizacoes/tipos-frota/${id}`)
  },

  // ── Categorias ────────────────────────────────────────────────────────────
  async listarCategorias(): Promise<CategoriaItem[]> {
    const { data } = await api.get<any[]>('/parametrizacoes/categorias')
    return data.map((x) => ({ id: x.id, nome: x.nome, descricao: x.descricao ?? '', ativo: x.ativa }))
  },
  async criarCategoria(data: CategoriaLookupPayload): Promise<void> {
    await api.post('/parametrizacoes/categorias', toAtivaPayload(data))
  },
  async atualizarCategoria(id: number, data: CategoriaLookupPayload): Promise<void> {
    await api.patch(`/parametrizacoes/categorias/${id}`, toAtivaPayload(data))
  },
  async excluirCategoria(id: number): Promise<void> {
    await api.delete(`/parametrizacoes/categorias/${id}`)
  },

  // ── Tipos de Veículo ──────────────────────────────────────────────────────
  async listarTiposVeiculo(): Promise<LookupItem[]> {
    const { data } = await api.get<any[]>('/parametrizacoes/tipos-veiculo')
    return data.map((x) => ({ id: x.id, nome: x.nome, ativo: x.ativo }))
  },
  async criarTipoVeiculo(data: LookupPayload): Promise<void> {
    await api.post('/parametrizacoes/tipos-veiculo', toAtivoPayload(data))
  },
  async atualizarTipoVeiculo(id: number, data: LookupPayload): Promise<void> {
    await api.patch(`/parametrizacoes/tipos-veiculo/${id}`, toAtivoPayload(data))
  },
  async excluirTipoVeiculo(id: number): Promise<void> {
    await api.delete(`/parametrizacoes/tipos-veiculo/${id}`)
  },

  // ── Marcas ────────────────────────────────────────────────────────────────
  async listarMarcas(): Promise<LookupItem[]> {
    const { data } = await api.get<any[]>('/parametrizacoes/marcas')
    return data.map((x) => ({ id: x.id, nome: x.nome, ativo: x.ativo }))
  },
  async criarMarca(data: LookupPayload): Promise<void> {
    await api.post('/parametrizacoes/marcas', toAtivoPayload(data))
  },
  async atualizarMarca(id: number, data: LookupPayload): Promise<void> {
    await api.patch(`/parametrizacoes/marcas/${id}`, toAtivoPayload(data))
  },
  async excluirMarca(id: number): Promise<void> {
    await api.delete(`/parametrizacoes/marcas/${id}`)
  },

  // ── Modelos ───────────────────────────────────────────────────────────────
  async listarModelos(): Promise<ModeloItem[]> {
    const { data } = await api.get<any[]>('/parametrizacoes/modelos')
    return data.map((x) => ({ id: x.id, nome: x.nome, marca_id: x.marca_id, ativo: x.ativo }))
  },
  async criarModelo(data: ModeloPayload): Promise<void> {
    await api.post('/parametrizacoes/modelos', toAtivoPayload(data))
  },
  async atualizarModelo(id: number, data: ModeloPayload): Promise<void> {
    await api.patch(`/parametrizacoes/modelos/${id}`, toAtivoPayload(data))
  },
  async excluirModelo(id: number): Promise<void> {
    await api.delete(`/parametrizacoes/modelos/${id}`)
  },

  // ── Combustíveis ──────────────────────────────────────────────────────────
  async listarCombustiveis(): Promise<LookupItem[]> {
    const { data } = await api.get<any[]>('/parametrizacoes/combustiveis')
    return data.map((x) => ({ id: x.id, nome: x.nome, ativo: x.ativo }))
  },
  async criarCombustivel(data: LookupPayload): Promise<void> {
    await api.post('/parametrizacoes/combustiveis', toAtivoPayload(data))
  },
  async atualizarCombustivel(id: number, data: LookupPayload): Promise<void> {
    await api.patch(`/parametrizacoes/combustiveis/${id}`, toAtivoPayload(data))
  },
  async excluirCombustivel(id: number): Promise<void> {
    await api.delete(`/parametrizacoes/combustiveis/${id}`)
  },
}
