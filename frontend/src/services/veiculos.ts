import api from './api'
import type {
  Marca, Modelo, TipoVeiculo, Veiculo, VeiculoListItem,
  Categoria, TipoFrota, Unidade, Subunidade, CentroCusto
} from '@/types'

interface VeiculoFilters {
  q?: string
  situacao?: string
  categoria_id?: number
  tipo_frota_id?: number
  secretaria_id?: number
  unidade_id?: number
  centro_custo_id?: number
  skip?: number
  limit?: number
}

export const veiculoService = {
  // ── Veículos ───────────────────────────────────────────────────────────────

  async listar(filters: VeiculoFilters = {}): Promise<VeiculoListItem[]> {
    const response = await api.get<VeiculoListItem[]>('/veiculos', { params: filters })
    return response.data
  },

  async detalhe(id: number): Promise<Veiculo> {
    const response = await api.get<Veiculo>(`/veiculos/${id}`)
    return response.data
  },

  async criar(data: Partial<Veiculo>): Promise<Veiculo> {
    const response = await api.post<Veiculo>('/veiculos', data)
    return response.data
  },

  async atualizar(id: number, data: Partial<Veiculo>): Promise<Veiculo> {
    const response = await api.patch<Veiculo>(`/veiculos/${id}`, data)
    return response.data
  },

  async excluir(id: number): Promise<void> {
    await api.delete(`/veiculos/${id}`)
  },

  async ativar(id: number): Promise<Veiculo> {
    const response = await api.post<Veiculo>(`/veiculos/${id}/ativar`)
    return response.data
  },

  async inativar(id: number): Promise<Veiculo> {
    const response = await api.post<Veiculo>(`/veiculos/${id}/inativar`)
    return response.data
  },

  // ── Parametrizações ───────────────────────────────────────────────────────

  async categorias(): Promise<Categoria[]> {
    const response = await api.get<Categoria[]>('/veiculos/parametrizacoes/categorias')
    return response.data
  },

  async tiposFrota(): Promise<TipoFrota[]> {
    const response = await api.get<TipoFrota[]>('/veiculos/parametrizacoes/tipos-frota')
    return response.data
  },

  async unidades(secretariaId?: number): Promise<Unidade[]> {
    const params = secretariaId ? { secretaria_id: secretariaId } : {}
    const response = await api.get<Unidade[]>('/veiculos/parametrizacoes/unidades', { params })
    return response.data
  },

  async subunidades(unidadeId?: number): Promise<Subunidade[]> {
    const params = unidadeId ? { unidade_id: unidadeId } : {}
    const response = await api.get<Subunidade[]>('/veiculos/parametrizacoes/subunidades', { params })
    return response.data
  },

  async centrosCusto(): Promise<CentroCusto[]> {
    const response = await api.get<CentroCusto[]>('/veiculos/parametrizacoes/centros-custo')
    return response.data
  },

  // ── Base ────────────────────────────────────────────────────────────────────

  async marcas(): Promise<Marca[]> {
    const response = await api.get<Marca[]>('/veiculos/marcas')
    return response.data
  },

  async modelos(marcaId: number): Promise<Modelo[]> {
    const response = await api.get<Modelo[]>('/veiculos/modelos', { params: { marca_id: marcaId } })
    return response.data
  },

  async tiposVeiculo(): Promise<TipoVeiculo[]> {
    const response = await api.get<TipoVeiculo[]>('/veiculos/tipos-veiculo')
    return response.data
  },
}
