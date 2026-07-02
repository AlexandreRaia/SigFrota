import React, { useState } from 'react'
import { Upload } from 'lucide-react'
import type { Veiculo } from '@/types'

interface VehicleFilesTabProps {
  vehicle: Veiculo
  isEditMode: boolean
  onEditChange: (field: string, value: any) => void
}

export default function VehicleFilesTab({
  vehicle,
  isEditMode,
  onEditChange,
}: VehicleFilesTabProps) {
  const [isDragging, setIsDragging] = useState(false)

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }

  return (
    <div className="p-6">
      {/* Upload Area */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`rounded-lg border-2 border-dashed p-8 text-center transition-all mb-6 ${
          isDragging
            ? 'border-blue-500 bg-blue-500/10'
            : 'border-gray-300 dark:border-gray-600'
        }`}
      >
        <div className="flex flex-col items-center gap-3">
          <Upload className="w-6 h-6 text-blue-600 dark:text-blue-400" />
          <div>
            <p className="font-semibold text-gray-900 dark:text-white">Arraste arquivos aqui</p>
            <p className="text-sm text-gray-600 dark:text-gray-400">ou clique para selecionar</p>
          </div>
          <button className="mt-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-sm font-medium">
            Selecionar Arquivo
          </button>
        </div>
      </div>

      {/* Arquivos */}
      <div>
        <label className="block text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-4">
          Arquivos do Veículo
        </label>
        <p className="text-base font-medium text-gray-900 dark:text-gray-100">
          Nenhum arquivo adicionado
        </p>
      </div>
    </div>
  )
}
