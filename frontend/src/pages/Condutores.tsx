import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { condutorService } from '@/services/condutores'
import { Badge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'

export default function Condutores() {
  const [q, setQ] = useState('')
  const [status, setStatus] = useState('')

  const { data: condutores, isLoading } = useQuery({
    queryKey: ['condutores', { q, status }],
    queryFn: () => condutorService.listar({ q, status }),
  })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-slate-800">Condutores</h1>
        <Button>+ Novo Condutor</Button>
      </div>

      <div className="card p-4 flex gap-3">
        <input
          type="text"
          placeholder="Buscar por nome, CPF, prontuário..."
          className="input max-w-xs"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <select className="input max-w-xs" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">Todos os status</option>
          <option value="ATIVO">Ativo</option>
          <option value="INATIVO">Inativo</option>
          <option value="SUSPENSO">Suspenso</option>
        </select>
      </div>

      <div className="card overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Prontuário</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Nome</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">CPF</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Cargo</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">CNH</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 bg-white">
            {isLoading ? (
              <tr><td colSpan={6} className="py-10 text-center text-gray-400">Carregando...</td></tr>
            ) : condutores?.length === 0 ? (
              <tr><td colSpan={6} className="py-10 text-center text-gray-400">Nenhum condutor encontrado</td></tr>
            ) : (
              condutores?.map((c) => (
                <tr key={c.id} className="hover:bg-gray-50 cursor-pointer">
                  <td className="px-4 py-3 font-mono text-sm font-medium text-slate-800">{c.prontuario}</td>
                  <td className="px-4 py-3 text-sm font-medium text-slate-800">{c.nome}</td>
                  <td className="px-4 py-3 font-mono text-sm text-slate-600">{c.cpf}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">{c.cargo}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">{c.cnh_categoria}</td>
                  <td className="px-4 py-3">
                    <Badge variant={c.status === 'ATIVO' ? 'success' : c.status === 'SUSPENSO' ? 'warning' : 'danger'}>
                      {c.status}
                    </Badge>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
