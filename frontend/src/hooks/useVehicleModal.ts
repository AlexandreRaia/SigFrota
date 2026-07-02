import { useState, useCallback } from 'react'
import type { Veiculo } from '@/types'

interface UseVehicleModalReturn {
  isOpen: boolean
  vehicle: Veiculo | null
  openModal: (vehicle: Veiculo) => void
  closeModal: () => void
}

export function useVehicleModal(): UseVehicleModalReturn {
  const [isOpen, setIsOpen] = useState(false)
  const [vehicle, setVehicle] = useState<Veiculo | null>(null)

  const openModal = useCallback((vehicleData: Veiculo) => {
    setVehicle(vehicleData)
    setIsOpen(true)
  }, [])

  const closeModal = useCallback(() => {
    setIsOpen(false)
    setTimeout(() => setVehicle(null), 300) // Wait for animation
  }, [])

  return {
    isOpen,
    vehicle,
    openModal,
    closeModal,
  }
}
