import api from './api'
import type { LoginRequest, TokenResponse, Usuario } from '@/types'

export const authService = {
  async login(data: LoginRequest): Promise<TokenResponse> {
    const response = await api.post<TokenResponse>('/auth/login', data)
    return response.data
  },

  async me(): Promise<Usuario> {
    const response = await api.get<Usuario>('/auth/me')
    return response.data
  },

  logout(): void {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },
}
