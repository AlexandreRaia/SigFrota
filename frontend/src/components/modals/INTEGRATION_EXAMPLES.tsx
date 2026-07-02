/**
 * EXEMPLO DE INTEGRAÇÃO DO MODAL
 * 
 * Este arquivo demonstra como integrar o modal unificado de veículos
 * na página de Veículos existente. Copie este código como referência.
 */

import React, { useState } from 'react'
import { useVehicleModal } from '@/hooks/useVehicleModal'
import VehicleDetailModal from '@/components/modals/VehicleDetailModal'
import type { Veiculo } from '@/types'

/**
 * EXEMPLO 1: Integração no componente de tabela
 * 
 * Adicione isto ao seu componente VeiculosPage ou similar
 */
export function VeiculosPageExample() {
  const { isOpen, vehicle, openModal, closeModal } = useVehicleModal()
  const [veiculos, setVeiculos] = useState<Veiculo[]>([])

  const handleViewVehicle = (veiculo: Veiculo) => {
    openModal(veiculo)
  }

  const handleSaveVehicle = async (updatedVehicle: Veiculo) => {
    try {
      // Chamar sua API para salvar
      // await veiculoService.update(updatedVehicle.id, updatedVehicle)
      
      // Atualizar lista local
      setVeiculos(veiculos.map(v => 
        v.id === updatedVehicle.id ? updatedVehicle : v
      ))
      
      closeModal()
    } catch (error) {
      console.error('Erro ao salvar veículo:', error)
      // Mostrar toast de erro
    }
  }

  return (
    <>
      {/* Sua tabela de veículos */}
      <table className="w-full">
        <thead>
          <tr>
            <th>Placa</th>
            <th>Marca/Modelo</th>
            <th>Status</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          {veiculos.map(veiculo => (
            <tr key={veiculo.id}>
              <td>{veiculo.placa}</td>
              <td>{veiculo.marca?.nome} {veiculo.modelo?.nome}</td>
              <td>
                <span className={`px-2 py-1 rounded text-sm ${
                  veiculo.situacao === 'Ativo'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-red-100 text-red-800'
                }`}>
                  {veiculo.situacao}
                </span>
              </td>
              <td>
                <button 
                  onClick={() => handleViewVehicle(veiculo)}
                  className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Ver / Editar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal - Renderize onde quiser na página */}
      {vehicle && (
        <VehicleDetailModal
          vehicle={vehicle}
          isOpen={isOpen}
          onClose={closeModal}
          onSave={handleSaveVehicle}
        />
      )}
    </>
  )
}

/**
 * EXEMPLO 2: Botão reutilizável para abrir modal
 */
interface ViewVehicleButtonProps {
  vehicle: Veiculo
  onSave?: (vehicle: Veiculo) => Promise<void>
}

export function ViewVehicleButton({ vehicle, onSave }: ViewVehicleButtonProps) {
  const { isOpen, openModal, closeModal } = useVehicleModal()

  return (
    <>
      <button
        onClick={() => openModal(vehicle)}
        className="flex items-center gap-2 px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors text-sm"
      >
        👁️ Ver / Editar
      </button>

      <VehicleDetailModal
        vehicle={vehicle}
        isOpen={isOpen}
        onClose={closeModal}
        onSave={onSave}
      />
    </>
  )
}

/**
 * EXEMPLO 3: Usando em um card de veículo
 */
export function VehicleCard({ vehicle }: { vehicle: Veiculo }) {
  const { isOpen, openModal, closeModal } = useVehicleModal()

  return (
    <>
      <div
        onClick={() => openModal(vehicle)}
        className="p-4 rounded-lg border border-gray-200 hover:shadow-lg cursor-pointer transition-all"
      >
        <h3 className="font-bold text-lg">{vehicle.placa}</h3>
        <p className="text-gray-600">
          {vehicle.marca?.nome} {vehicle.modelo?.nome}
        </p>
        <p className="text-sm text-gray-500">
          Ano: {vehicle.ano_fabricacao}
        </p>
      </div>

      <VehicleDetailModal
        vehicle={vehicle}
        isOpen={isOpen}
        onClose={closeModal}
      />
    </>
  )
}

/**
 * EXEMPLO 4: Integração com React Query
 */
import { useMutation, useQueryClient } from '@tanstack/react-query'

export function VeiculosPageWithReactQuery() {
  const { isOpen, vehicle, openModal, closeModal } = useVehicleModal()
  const queryClient = useQueryClient()

  // Mutation para salvar veículo
  const updateMutation = useMutation({
    mutationFn: async (updatedVehicle: Veiculo) => {
      // const response = await api.patch(`/veiculos/${updatedVehicle.id}`, updatedVehicle)
      // return response.data
      return updatedVehicle
    },
    onSuccess: () => {
      // Invalidar cache de veículos
      queryClient.invalidateQueries({ queryKey: ['veiculos'] })
      closeModal()
    },
    onError: (error) => {
      console.error('Erro ao atualizar:', error)
    },
  })

  return (
    <>
      {vehicle && (
        <VehicleDetailModal
          vehicle={vehicle}
          isOpen={isOpen}
          onClose={closeModal}
          onSave={(updatedVehicle) => updateMutation.mutateAsync(updatedVehicle)}
        />
      )}
    </>
  )
}

/**
 * EXEMPLO 5: Customização de salvamento
 */
export function CustomSaveExample() {
  const { isOpen, vehicle, openModal, closeModal } = useVehicleModal()
  const [isSaving, setIsSaving] = useState(false)

  const handleCustomSave = async (updatedVehicle: Veiculo) => {
    setIsSaving(true)
    try {
      // Validação customizada
      if (!updatedVehicle.placa) {
        throw new Error('Placa é obrigatória')
      }

      // Transformação de dados antes de salvar
      const dataToSave = {
        ...updatedVehicle,
        // Adicionar campos específicos ou transformações
      }

      // Salvar via API
      // await veiculoService.update(dataToSave.id, dataToSave)

      // Log de auditoria
      console.log('Veículo atualizado:', dataToSave)

      closeModal()
    } catch (error) {
      console.error('Erro customizado:', error)
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <>
      {vehicle && (
        <VehicleDetailModal
          vehicle={vehicle}
          isOpen={isOpen}
          onClose={closeModal}
          onSave={handleCustomSave}
        />
      )}
    </>
  )
}
