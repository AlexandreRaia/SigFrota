import api from './api'
import type { Condutor, CondutorListItem, CondutorDocumento, Unidade, Subunidade } from '@/types'

interface CondutorFilters {
  q?: string
  status?: string
  unidade_id?: number
  skip?: number
  limit?: number
}

export interface UnidadeItem {
  id: number
  nome: string
  sigla: string
  ativa: boolean
}

export const condutorService = {
  async listar(filters: CondutorFilters = {}): Promise<CondutorListItem[]> {
    const response = await api.get<CondutorListItem[]>('/condutores', { params: filters })
    return response.data
  },

  async detalhe(id: number): Promise<Condutor> {
    const response = await api.get<Condutor>(`/condutores/${id}`)
    return response.data
  },

  async criar(data: Partial<Condutor>): Promise<Condutor> {
    const response = await api.post<Condutor>('/condutores', data)
    return response.data
  },

  async atualizar(id: number, data: Partial<Condutor>): Promise<Condutor> {
    const response = await api.patch<Condutor>(`/condutores/${id}`, data)
    return response.data
  },

  async ativar(id: number): Promise<Condutor> {
    const response = await api.patch<Condutor>(`/condutores/${id}/ativar`)
    return response.data
  },

  async inativar(id: number): Promise<Condutor> {
    const response = await api.patch<Condutor>(`/condutores/${id}/inativar`)
    return response.data
  },

  async excluir(id: number): Promise<void> {
    await api.delete(`/condutores/${id}`)
  },

  async secretarias(): Promise<UnidadeItem[]> {
    return this.unidades()
  },

  async unidades(): Promise<Unidade[]> {
    const response = await api.get<Unidade[]>('/condutores/parametrizacoes/unidades')
    return response.data
  },

  async subunidades(unidadeId?: number): Promise<Subunidade[]> {
    const params = unidadeId ? { unidade_id: unidadeId } : {}
    const response = await api.get<Subunidade[]>('/condutores/parametrizacoes/subunidades', { params })
    return response.data
  },

  async listarDocumentos(condutorId: number): Promise<CondutorDocumento[]> {
    const response = await api.get<CondutorDocumento[]>(`/condutores/${condutorId}/documentos`)
    return response.data
  },

  async uploadDocumento(condutorId: number, tipo: string, descricao: string, arquivo: File): Promise<CondutorDocumento> {
    const form = new FormData()
    form.append('tipo', tipo)
    form.append('descricao', descricao)
    form.append('arquivo', arquivo)
    const response = await api.post<CondutorDocumento>(`/condutores/${condutorId}/documentos`, form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  },

  async deletarDocumento(condutorId: number, docId: number): Promise<void> {
    await api.delete(`/condutores/${condutorId}/documentos/${docId}`)
  },
}
