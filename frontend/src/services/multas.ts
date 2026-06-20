import api from './api'
import type { Multa, MultaListItem } from '@/types'

interface MultaFilters {
  q?: string
  status?: string
  condutor_id?: number
  skip?: number
  limit?: number
}

export const multaService = {
  async listar(filters: MultaFilters = {}): Promise<MultaListItem[]> {
    const response = await api.get<MultaListItem[]>('/multas', { params: filters })
    return response.data
  },

  async detalhe(id: number): Promise<Multa> {
    const response = await api.get<Multa>(`/multas/${id}`)
    return response.data
  },

  async criar(data: Partial<Multa>): Promise<Multa> {
    const response = await api.post<Multa>('/multas', data)
    return response.data
  },

  async atualizar(id: number, data: Partial<Multa>): Promise<Multa> {
    const response = await api.patch<Multa>(`/multas/${id}`, data)
    return response.data
  },

  async excluir(id: number): Promise<void> {
    await api.delete(`/multas/${id}`)
  },
}
