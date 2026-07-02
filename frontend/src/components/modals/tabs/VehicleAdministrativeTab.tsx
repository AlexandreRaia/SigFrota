import React from 'react'
import type { Veiculo } from '@/types'

interface VehicleAdministrativeTabProps {
  vehicle: Veiculo
  isEditMode: boolean
  onEditChange: (field: string, value: any) => void
}

// Simple DataField component for clean display
const DataField: React.FC<{ label: string; value: any }> = ({ label, value }) => (
  <div className="border-b border-gray-100 dark:border-gray-700/50 pb-4">
    <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2">
      {label}
    </label>
    <p className="text-base font-medium text-gray-900 dark:text-gray-100">
      {value || '—'}
    </p>
  </div>
)

export default function VehicleAdministrativeTab({
  vehicle,
  isEditMode,
  onEditChange,
}: VehicleAdministrativeTabProps) {
  const formatDate = (date: string | undefined) => {
    if (!date) return '—'
    return new Date(date).toLocaleDateString('pt-BR')
  }

  const isSecurityActive = vehicle.vencimento_seguro && new Date(vehicle.vencimento_seguro) > new Date()

  return (
    <div className="p-6">
      <div className="grid grid-cols-2 gap-6">
        {/* Aquisição e Propriedade */}
        <DataField label="Valor de Aquisição" value={vehicle.valor_aquisicao ? `R$ ${vehicle.valor_aquisicao}` : '—'} />
        <DataField label="Tipo de Aquisição" value={vehicle.tipo_aquisicao} />
        <DataField label="Tipo de Convênio" value={vehicle.tipo_convenio} />
        <DataField label="Nome Locador/Proprietário" value={vehicle.nome_locador} />

        {/* Seguro */}
        <DataField label="Vencimento do Seguro" value={formatDate(vehicle.vencimento_seguro)} />
        <DataField label="Valor da Locação (mensal)" value={vehicle.valor_locacao ? `R$ ${vehicle.valor_locacao}` : '—'} />

        {/* Localização e Alocação */}
        <DataField label="Secretaria" value={vehicle.secretaria?.nome} />
        <DataField label="Unidade" value={vehicle.unidade?.nome} />
        <DataField label="Subunidade" value={vehicle.subunidade?.nome} />
        <DataField label="Centro de Custo" value={vehicle.centro_custo?.nome} />

        {/* Histórico */}
        <DataField label="Data de Criação" value={formatDate(vehicle.criado_em)} />
        <DataField label="Última Atualização" value={formatDate(vehicle.atualizado_em)} />
      </div>
    </div>
  )
}
