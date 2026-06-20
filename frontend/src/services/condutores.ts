import api from './api'
import type { Condutor, CondutorListItem } from '@/types'

interface CondutorFilters {
  q?: string
  status?: string
  secretaria_id?: number
  skip?: number
  limit?: number
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

  async excluir(id: number): Promise<void> {
    await api.delete(`/condutores/${id}`)
  },
}
