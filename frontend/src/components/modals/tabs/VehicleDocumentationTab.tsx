import React from 'react'
import type { Veiculo } from '@/types'

interface VehicleDocumentationTabProps {
  vehicle: Veiculo
  isEditMode: boolean
  onEditChange: (field: string, value: any) => void
}

const getStatusColor = (date: string | null | undefined) => {
  if (!date) return 'text-gray-600'
  const daysUntil = Math.ceil((new Date(date).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24))
  if (daysUntil < 0) return 'text-red-600'
  if (daysUntil < 30) return 'text-yellow-600'
  return 'text-emerald-600'
}

const getStatusLabel = (date: string | null | undefined) => {
  if (!date) return 'Não informado'
  const daysUntil = Math.ceil((new Date(date).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24))
  if (daysUntil < 0) return `Vencido (${Math.abs(daysUntil)} dias)`
  if (daysUntil < 30) return `Vence em ${daysUntil} dias`
  return `Válido até ${new Date(date).toLocaleDateString('pt-BR')}`
}

// Simple DataField component for clean display
const DataField: React.FC<{ label: string; value: any; status?: string }> = ({ label, value, status }) => (
  <div className="border-b border-gray-100 dark:border-gray-700/50 pb-4">
    <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2">
      {label}
    </label>
    <p className="text-base font-medium text-gray-900 dark:text-gray-100">
      {value || '—'}
    </p>
    {status && (
      <p className={`text-xs mt-1 ${status}`}>
        {getStatusLabel(value)}
      </p>
    )}
  </div>
)

export default function VehicleDocumentationTab({
  vehicle,
  isEditMode,
  onEditChange,
}: VehicleDocumentationTabProps) {
  const formatDate = (date: string | undefined) => {
    if (!date) return '—'
    return new Date(date).toLocaleDateString('pt-BR')
  }

  return (
    <div className="p-6">
      <div className="grid grid-cols-2 gap-6">
        {/* Vencimentos */}
        <DataField 
          label="Vencimento CRLV" 
          value={formatDate(vehicle.vencimento_licenciamento)}
          status={getStatusColor(vehicle.vencimento_licenciamento)}
        />
        <DataField 
          label="Vencimento Seguro" 
          value={formatDate(vehicle.vencimento_seguro)}
          status={getStatusColor(vehicle.vencimento_seguro)}
        />
        <DataField 
          label="Vencimento IPVA" 
          value={formatDate(vehicle.vencimento_ipva)}
          status={getStatusColor(vehicle.vencimento_ipva)}
        />
      </div>
    </div>
  )
}
