import { useQuery } from '@tanstack/react-query'
import { manutencaoService } from '@/services/manutencao'
import { veiculoService } from '@/services/veiculos'

function KpiCard({ label, value, icon, color }: { label: string; value: number | string; icon: string; color: string }) {
  return (
    <div className={`card p-6 border-l-4 ${color}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-slate-500">{label}</p>
          <p className="mt-1 text-2xl font-bold text-slate-800">{value}</p>
        </div>
        <span className="text-3xl">{icon}</span>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const { data: dashSMV } = useQuery({
    queryKey: ['manutencao', 'dashboard'],
    queryFn: () => manutencaoService.dashboard(),
  })

  const { data: veiculos } = useQuery({
    queryKey: ['veiculos', 'lista'],
    queryFn: () => veiculoService.listar({ limit: 1000 }),
  })

  const totalVeiculos = veiculos?.length ?? 0
  const emManutencao = veiculos?.filter((v) => v.situacao === 'MANUTENCAO').length ?? 0
  const disponiveis = veiculos?.filter((v) => v.situacao === 'ATIVO').length ?? 0

  return (
    <div className="space-y-6">
      <h1 className="text-xl font-bold text-slate-800">Dashboard</h1>

      {/* KPIs */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard label="Total de Veículos" value={totalVeiculos} icon="🚗" color="border-blue-500" />
        <KpiCard label="Disponíveis" value={disponiveis} icon="✅" color="border-green-500" />
        <KpiCard label="Em Manutenção" value={emManutencao} icon="🔧" color="border-yellow-500" />
        <KpiCard label="SMVs em Aberto" value={dashSMV?.em_aberto ?? '—'} icon="📋" color="border-red-500" />
      </div>

      {/* SMV por etapa */}
      {dashSMV?.por_etapa && (
        <div className="card p-6">
          <h2 className="mb-4 text-base font-semibold text-slate-800">Manutenções por Etapa</h2>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-4 lg:grid-cols-9">
            {Object.entries(dashSMV.por_etapa).map(([etapa, count]) => (
              <div key={etapa} className="rounded-lg bg-gray-50 p-3 text-center">
                <p className="text-2xl font-bold text-primary-600">{count}</p>
                <p className="mt-1 text-xs text-gray-500">{etapa}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
