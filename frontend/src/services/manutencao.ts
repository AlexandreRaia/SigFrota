import api from './api'
import type { SMV, SMVListItem } from '@/types'

interface SMVFilters {
  q?: string
  etapa?: string
  urgencia?: string
  skip?: number
  limit?: number
}

export const manutencaoService = {
  async listar(filters: SMVFilters = {}): Promise<SMVListItem[]> {
    const response = await api.get<SMVListItem[]>('/manutencao', { params: filters })
    return response.data
  },

  async detalhe(id: number): Promise<SMV> {
    const response = await api.get<SMV>(`/manutencao/${id}`)
    return response.data
  },

  async criar(data: { veiculo_id: number; descricao_problema: string; urgencia?: string; km_entrada?: number }): Promise<SMV> {
    const response = await api.post<SMV>('/manutencao', data)
    return response.data
  },

  async avancarEtapa(id: number, etapa_para: string, observacao = ''): Promise<SMV> {
    const response = await api.post<SMV>(`/manutencao/${id}/avancar`, { etapa_para, observacao })
    return response.data
  },

  async dashboard(): Promise<{ total: number; em_aberto: number; finalizadas: number; por_etapa: Record<string, number> }> {
    const response = await api.get('/manutencao/dashboard')
    return response.data
  },

  async mensagens(smvId: number) {
    const response = await api.get(`/chat/smv/${smvId}`)
    return response.data
  },

  async enviarMensagem(smvId: number, texto: string) {
    const response = await api.post(`/chat/smv/${smvId}`, { texto })
    return response.data
  },
}
