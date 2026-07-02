import React from 'react'
import type { Veiculo } from '@/types'
import VehicleGeneralTab from './tabs/VehicleGeneralTab'
import VehicleFleetTab from './tabs/VehicleFleetTab'
import VehicleTechnicalTab from './tabs/VehicleTechnicalTab'
import VehicleAdministrativeTab from './tabs/VehicleAdministrativeTab'
import VehicleOperationalTab from './tabs/VehicleOperationalTab'
import VehicleDocumentationTab from './tabs/VehicleDocumentationTab'
import VehicleFilesTab from './tabs/VehicleFilesTab'

interface VehicleDataPanelProps {
  activeTab: string
  vehicle: Veiculo
  isEditMode: boolean
  onEditChange: (field: string, value: any) => void
}

export default function VehicleDataPanel({
  activeTab,
  vehicle,
  isEditMode,
  onEditChange,
}: VehicleDataPanelProps) {
  return (
    <div className="p-6">
      {activeTab === 'gerais' && (
        <VehicleGeneralTab
          vehicle={vehicle}
          isEditMode={isEditMode}
          onEditChange={onEditChange}
        />
      )}
      {activeTab === 'frota' && (
        <VehicleFleetTab
          vehicle={vehicle}
          isEditMode={isEditMode}
          onEditChange={onEditChange}
        />
      )}
      {activeTab === 'tecnico' && (
        <VehicleTechnicalTab
          vehicle={vehicle}
          isEditMode={isEditMode}
          onEditChange={onEditChange}
        />
      )}
      {activeTab === 'administrativa' && (
        <VehicleAdministrativeTab
          vehicle={vehicle}
          isEditMode={isEditMode}
          onEditChange={onEditChange}
        />
      )}
      {activeTab === 'operacional' && (
        <VehicleOperationalTab
          vehicle={vehicle}
          isEditMode={isEditMode}
          onEditChange={onEditChange}
        />
      )}
      {activeTab === 'documentacao' && (
        <VehicleDocumentationTab
          vehicle={vehicle}
          isEditMode={isEditMode}
          onEditChange={onEditChange}
        />
      )}
      {activeTab === 'arquivos' && (
        <VehicleFilesTab
          vehicle={vehicle}
          isEditMode={isEditMode}
          onEditChange={onEditChange}
        />
      )}
    </div>
  )
}
