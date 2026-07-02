import React from 'react'
import type { Veiculo } from '@/types'
import EditableField from '../EditableField'

interface VehicleGeneralTabProps {
  vehicle: Veiculo
  isEditMode: boolean
  onEditChange: (field: string, value: any) => void
}

// Componente para exibir campo de forma limpa
const DataField = ({ label, value, icon }: { label: string; value: any; icon?: string }) => (
  <div className="pb-4 border-b border-gray-100 dark:border-gray-800 last:border-b-0">
    <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-1.5">
      {icon && <span className="mr-1">{icon}</span>}{label}
    </p>
    <p className="text-base font-medium text-gray-900 dark:text-white">
      {value || '—'}
    </p>
  </div>
)

export default function VehicleGeneralTab({
  vehicle,
  isEditMode,
  onEditChange,
}: VehicleGeneralTabProps) {
  return (
    <div className="max-w-2xl space-y-5">
      <div className="grid grid-cols-2 gap-6">
        {/* Placa */}
        <div>
          <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2">
            Placa
          </label>
          <p className="text-lg font-bold text-gray-900 dark:text-white font-mono">
            {vehicle.placa || '—'}
          </p>
        </div>

        {/* Prefixo */}
        <div>
          <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2">
            Prefixo
          </label>
          <p className="text-lg font-bold text-gray-900 dark:text-white">
            {vehicle.prefixo || '—'}
          </p>
        </div>

        {/* Marca */}
        <DataField label="Marca" value={vehicle.marca?.nome} />

        {/* Modelo */}
        <DataField label="Modelo" value={vehicle.modelo?.nome} />

        {/* Ano de Fabricação */}
        <DataField label="Ano Fabricação" value={vehicle.ano_fabricacao} />

        {/* Ano Modelo */}
        <DataField label="Ano Modelo" value={vehicle.ano_modelo} />

        {/* Cor */}
        <DataField label="Cor" value={vehicle.cor} />

        {/* Combustível */}
        <DataField label="Combustível" value={vehicle.combustivel} />

        {/* Motorização */}
        <div className="col-span-2">
          <DataField label="Motorização" value={vehicle.motorizacao} />
        </div>

        {/* RENAVAM */}
        <div className="col-span-2">
          <DataField label="RENAVAM" value={vehicle.renavam} />
        </div>

        {/* Chassi */}
        <div className="col-span-2">
          <DataField label="Chassi (VIN)" value={vehicle.chassi} />
        </div>

        {/* Observações */}
        {vehicle.observacoes && (
          <div className="col-span-2">
            <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2">
              Observações
            </label>
            <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
              {vehicle.observacoes}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
