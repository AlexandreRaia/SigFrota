import React from 'react'
import type { Veiculo } from '@/types'

interface VehicleOperationalTabProps {
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

export default function VehicleOperationalTab({
  vehicle,
  isEditMode,
  onEditChange,
}: VehicleOperationalTabProps) {
  return (
    <div className="p-6">
      <div className="grid grid-cols-2 gap-6">
        {/* Informações Operacionais */}
        <DataField label="Quilometragem Atual" value={vehicle.hodometro_horimetro_inicial ? `${vehicle.hodometro_horimetro_inicial} km` : '—'} />
        <DataField label="Tipo de Controle" value={vehicle.tipo_controle} />
        <DataField label="Status Operacional" value={vehicle.situacao} />
        <DataField label="Capacidade de Passageiros" value={vehicle.capacidade_passageiros} />

        {/* Condutores e Escala */}
        <div className="col-span-2">
          <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-3">
            Condutor Designado
          </label>
          <p className="text-base font-medium text-gray-900 dark:text-gray-100">—</p>
        </div>
      </div>
    </div>
  )
}
