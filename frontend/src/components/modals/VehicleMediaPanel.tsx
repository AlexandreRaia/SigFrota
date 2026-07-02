import React, { useState } from 'react'
import { Upload, Image as ImageIcon } from 'lucide-react'
import type { Veiculo } from '@/types'

interface VehicleMediaPanelProps {
  vehicle: Veiculo
  isEditMode?: boolean
}

export default function VehicleMediaPanel({ vehicle, isEditMode = false }: VehicleMediaPanelProps) {
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
    <div className="flex flex-col items-center justify-center h-full bg-gradient-to-br from-gray-900 via-gray-950 to-black p-6">
      {/* Vehicle Image Area - Simples e elegante */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`w-full h-full rounded-2xl overflow-hidden transition-all flex items-center justify-center relative group ${
          isDragging ? 'bg-blue-500/20' : 'bg-gray-900'
        }`}
      >
        {vehicle.foto ? (
          <>
            <img
              src={vehicle.foto}
              alt={`${vehicle.marca?.nome} ${vehicle.modelo?.nome}`}
              className="w-full h-full object-cover"
            />
            {isEditMode && (
              <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors">
                  <Upload size={16} />
                  <span>Trocar Foto</span>
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="flex flex-col items-center gap-4 text-gray-500">
            <div className="w-24 h-24 rounded-full bg-gray-800 flex items-center justify-center">
              <ImageIcon size={48} strokeWidth={1} />
            </div>
            <p className="text-sm font-medium text-gray-400">Nenhuma imagem</p>
            {isEditMode && (
              <>
                <p className="text-xs text-gray-600">Arraste para adicionar</p>
                <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors text-sm">
                  <Upload size={16} />
                  <span>Selecionar Foto</span>
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
