import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import type { Perfil } from '@/types'

interface ProtectedRouteProps {
  allowedPerfis?: Perfil[]
}

export function ProtectedRoute({ allowedPerfis }: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, user } = useAuth()

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary-600 border-t-transparent" />
      </div>
    )
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  if (allowedPerfis && user && !user.is_superuser && !allowedPerfis.includes(user.perfil)) {
    return <Navigate to="/acesso-negado" replace />
  }

  return <Outlet />
}
