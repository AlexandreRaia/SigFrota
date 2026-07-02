import React from 'react'
import type { Veiculo } from '@/types'

interface VehicleTechnicalTabProps {
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

export default function VehicleTechnicalTab({
  vehicle,
  isEditMode,
  onEditChange,
}: VehicleTechnicalTabProps) {
  return (
    <div className="p-6">
      <div className="grid grid-cols-2 gap-6">
        {/* Motor e Combustível */}
        <DataField label="Combustível" value={vehicle.combustivel} />
        <DataField label="Motorização" value={vehicle.motorizacao} />
        <DataField label="Cilindrada (cc)" value={vehicle.cilindrada} />
        <DataField label="Potência (cv)" value={vehicle.potencia} />
        <DataField label="Transmissão" value={vehicle.transmissao} />
        <DataField label="Tração" value={vehicle.tracao} />

        {/* Identificação */}
        <DataField label="Chassi (VIN)" value={vehicle.chassi} />
        <DataField label="RENAVAM" value={vehicle.renavam} />
        <DataField label="Número Patrimônio" value={vehicle.numero_patrimonio} />

        {/* Pneus */}
        <DataField label="Dimensão dos Pneus" value={vehicle.pneu_dimensao} />
        <DataField label="Índice de Velocidade" value={vehicle.pneu_velocidade} />
        <DataField label="Índice de Carga" value={vehicle.pneu_carga} />
        <DataField label="Capacidade do Tanque (L)" value={vehicle.capacidade_tanque} />

        {/* Conforto e Equipamentos */}
        <div className="col-span-2">
          <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-3">
            Equipamentos
          </label>
          <div className="flex gap-4">
            {[
              { key: 'vidros_eletricos', label: 'Vidros Elétricos' },
              { key: 'direcao', label: 'Direção Elétrica' },
              { key: 'ar_condicionado', label: 'Ar Condicionado' },
            ].map((item) => (
              <label key={item.key} className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={(vehicle as any)[item.key] || false}
                  onChange={(e) => onEditChange(item.key, e.target.checked)}
                  disabled={!isEditMode}
                  className="rounded"
                />
                <span className="text-sm text-gray-700 dark:text-gray-300">{item.label}</span>
              </label>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
