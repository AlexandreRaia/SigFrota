import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { multaService } from '@/services/multas'
import { StatusMultaBadge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'

export default function Multas() {
  const [q, setQ] = useState('')
  const [status, setStatus] = useState('')

  const { data: multas, isLoading } = useQuery({
    queryKey: ['multas', { q, status }],
    queryFn: () => multaService.listar({ q, status }),
  })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-slate-800">Multas</h1>
        <Button>+ Registrar Multa</Button>
      </div>

      <div className="card p-4 flex gap-3">
        <input
          type="text"
          placeholder="Buscar por placa..."
          className="input max-w-xs"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <select className="input max-w-xs" value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="">Todos os status</option>
          <option value="PENDENTE">Pendente</option>
          <option value="PAGA">Paga</option>
          <option value="CONTESTADA">Contestada</option>
          <option value="VENCIDA">Vencida</option>
        </select>
      </div>

      <div className="card overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Placa</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Data Infração</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Valor</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Pontos</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Vencimento</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 bg-white">
            {isLoading ? (
              <tr><td colSpan={6} className="py-10 text-center text-gray-400">Carregando...</td></tr>
            ) : multas?.length === 0 ? (
              <tr><td colSpan={6} className="py-10 text-center text-gray-400">Nenhuma multa encontrada</td></tr>
            ) : (
              multas?.map((m) => (
                <tr key={m.id} className="hover:bg-gray-50 cursor-pointer">
                  <td className="px-4 py-3 font-mono text-sm font-medium text-slate-800">{m.placa}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">
                    {new Date(m.data_infracao).toLocaleDateString('pt-BR')}
                  </td>
                  <td className="px-4 py-3 text-sm font-medium text-slate-800">
                    {Number(m.valor).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })}
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-600">{m.pontos}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">
                    {new Date(m.data_vencimento).toLocaleDateString('pt-BR')}
                  </td>
                  <td className="px-4 py-3"><StatusMultaBadge status={m.status} /></td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
