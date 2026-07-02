import React from 'react'
import type { Veiculo } from '@/types'

interface VehicleFleetTabProps {
  vehicle: Veiculo
  isEditMode: boolean
  onEditChange: (field: string, value: any) => void
}

const DataField = ({ label, value }: { label: string; value: any }) => (
  <div className="pb-4 border-b border-gray-100 dark:border-gray-800 last:border-b-0">
    <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1.5">
      {label}
    </p>
    <p className="text-base font-medium text-gray-900 dark:text-white">
      {value || '—'}
    </p>
  </div>
)

export default function VehicleFleetTab({
  vehicle,
  isEditMode,
  onEditChange,
}: VehicleFleetTabProps) {
  return (
    <div className="max-w-2xl space-y-5">
      <div className="grid grid-cols-2 gap-6">
        {/* Tipo de Veículo */}
        <DataField label="Tipo de Veículo" value={vehicle.tipo_veiculo?.nome} />

        {/* Categoria */}
        <DataField label="Categoria" value={vehicle.categoria?.nome} />

        {/* Tipo de Frota */}
        <DataField label="Tipo de Frota" value={vehicle.tipo_frota?.nome} />

        {/* Secretaria */}
        <DataField label="Secretaria" value={vehicle.secretaria?.nome} />

        {/* Unidade */}
        <DataField label="Unidade" value={vehicle.unidade?.nome} />

        {/* Centro de Custo */}
        <DataField label="Centro de Custo" value={vehicle.centro_custo?.codigo || '—'} />

        {/* Quilometragem */}
        <div className="col-span-2">
          <DataField label="Quilometragem" value={vehicle.hodometro_horimetro_inicial ? `${vehicle.hodometro_horimetro_inicial} km` : '—'} />
        </div>

        {/* Status de Disponibilidade */}
        <div className="col-span-2">
          <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2">
            Status de Disponibilidade
          </label>
          <div className="flex gap-2">
            <span className="px-3 py-1.5 text-sm font-medium rounded-lg bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400">
              ✓ Disponível
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}
