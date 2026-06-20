import { Routes, Route, Navigate } from 'react-router-dom'
import { ProtectedRoute } from './ProtectedRoute'
import { Layout } from '@/components/layout/Layout'
import Login from '@/pages/Login'
import Dashboard from '@/pages/Dashboard'
import Veiculos from '@/pages/Veiculos'
import Condutores from '@/pages/Condutores'
import Manutencao from '@/pages/Manutencao'
import Multas from '@/pages/Multas'
import NotFound from '@/pages/NotFound'

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route element={<ProtectedRoute />}>
        <Route element={<Layout />}>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/veiculos/*" element={<Veiculos />} />
          <Route path="/condutores/*" element={<Condutores />} />
          <Route path="/manutencao/*" element={<Manutencao />} />
          <Route path="/multas/*" element={<Multas />} />
        </Route>
      </Route>

      <Route
        path="/acesso-negado"
        element={
          <div className="flex h-screen items-center justify-center text-center">
            <div>
              <h1 className="text-2xl font-bold text-red-600">Acesso Negado</h1>
              <p className="mt-2 text-gray-600">Você não tem permissão para acessar esta página.</p>
            </div>
          </div>
        }
      />
      <Route path="*" element={<NotFound />} />
    </Routes>
  )
}
