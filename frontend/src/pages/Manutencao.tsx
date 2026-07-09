import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { manutencaoService } from '@/services/manutencao'
import { EtapaSMVBadge } from '@/components/ui/Badge'
import { Button } from '@/components/ui/Button'

const URGENCIA_CORES: Record<string, string> = {
  ALTA: 'text-red-600 font-semibold',
  MEDIA: 'text-yellow-600',
  BAIXA: 'text-gray-500',
}

export default function Manutencao() {
  const [q, setQ] = useState('')
  const [etapa, setEtapa] = useState('')
  const [urgencia, setUrgencia] = useState('')

  const { data: smvs, isLoading } = useQuery({
    queryKey: ['smvs', { q, etapa, urgencia }],
    queryFn: () => manutencaoService.listar({ q, etapa, urgencia }),
  })

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-slate-800">Manutenção (SMV)</h1>
        <Button>+ Nova SMV</Button>
      </div>

      <div className="card p-4 flex flex-wrap gap-3">
        <input
          type="text"
          placeholder="Buscar por número SMV..."
          className="input max-w-xs"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <select className="input max-w-xs" value={etapa} onChange={(e) => setEtapa(e.target.value)}>
          <option value="">Todas as etapas</option>
          {['SOLICITACAO','RECEPCAO','DIAGNOSTICO','ORCAMENTO','APROVACAO','EXECUCAO','RETIRADA','EMISSAO_NF','FINALIZADO'].map(e => (
            <option key={e} value={e}>{e}</option>
          ))}
        </select>
        <select className="input max-w-xs" value={urgencia} onChange={(e) => setUrgencia(e.target.value)}>
          <option value="">Todas as urgências</option>
          <option value="ALTA">Alta</option>
          <option value="MEDIA">Média</option>
          <option value="BAIXA">Baixa</option>
        </select>
      </div>

      <div className="card overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Número</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Veículo</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Etapa</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Urgência</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Solicitação</th>
              <th className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Msgs</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 bg-white">
            {isLoading ? (
              <tr><td colSpan={6} className="py-10 text-center text-gray-400">Carregando...</td></tr>
            ) : smvs?.length === 0 ? (
              <tr><td colSpan={6} className="py-10 text-center text-gray-400">Nenhuma SMV encontrada</td></tr>
            ) : (
              smvs?.map((s) => (
                <tr key={s.id} className="hover:bg-gray-50 cursor-pointer">
                  <td className="px-4 py-3 font-mono font-bold text-primary-600">{s.numero}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">#{s.veiculo_id}</td>
                  <td className="px-4 py-3"><EtapaSMVBadge etapa={s.etapa} /></td>
                  <td className={`px-4 py-3 ${URGENCIA_CORES[s.urgencia]}`}>{s.urgencia}</td>
                  <td className="px-4 py-3 text-sm text-slate-600">
                    {new Date(s.dt_solicitacao).toLocaleDateString('pt-BR')}
                  </td>
                  <td className="px-4 py-3">
                    {s.msgs_nao_lidas > 0 && (
                      <span className="inline-flex items-center justify-center rounded-full bg-red-500 text-white text-xs w-5 h-5">
                        {s.msgs_nao_lidas}
                      </span>
                    )}
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
