import React, { useState } from 'react'
import { X, Edit2, Save, ArrowLeft, MoreVertical, Camera, FileText, Truck, Wrench, File, Coins, Disc3, History, Fuel, Calendar, Car, Shield, Pencil, Circle, Users, Building, AlertCircle, Gauge } from 'lucide-react'
import type { Veiculo } from '@/types'
import VehicleGeneralTab from './tabs/VehicleGeneralTab'
import VehicleFleetTab from './tabs/VehicleFleetTab'
import VehicleTechnicalTab from './tabs/VehicleTechnicalTab'
import VehicleAdministrativeTab from './tabs/VehicleAdministrativeTab'
import VehicleOperationalTab from './tabs/VehicleOperationalTab'
import VehicleDocumentationTab from './tabs/VehicleDocumentationTab'
import VehicleFilesTab from './tabs/VehicleFilesTab'

interface VehicleDetailModalProps {
  vehicle: Veiculo
  isOpen: boolean
  onClose: () => void
  onSave?: (vehicle: Veiculo) => Promise<void>
}

type TabType = 'gerais' | 'frota' | 'tecnico' | 'administrativa' | 'operacional' | 'documentacao' | 'arquivos'

export default function VehicleDetailModal({
  vehicle,
  isOpen,
  onClose,
  onSave,
}: VehicleDetailModalProps) {
  const [activeTab, setActiveTab] = useState<TabType>('gerais')
  const [isEditMode, setIsEditMode] = useState(false)
  const [editedVehicle, setEditedVehicle] = useState(vehicle)
  const [isSaving, setIsSaving] = useState(false)

  if (!isOpen) return null

  const tabs: { id: TabType; label: string }[] = [
    { id: 'gerais', label: 'Dados Gerais' },
    { id: 'frota', label: 'Frota' },
    { id: 'tecnico', label: 'Manutenções' },
    { id: 'administrativa', label: 'Documentos' },
    { id: 'operacional', label: 'Abastecimentos' },
    { id: 'documentacao', label: 'Pneus' },
    { id: 'arquivos', label: 'Histórico' },
  ]

  const handleEditChange = (field: string, value: any) => {
    setEditedVehicle({
      ...editedVehicle,
      [field]: value,
    })
  }

  const handleSave = async () => {
    if (!onSave) return
    try {
      setIsSaving(true)
      await onSave(editedVehicle)
      setIsEditMode(false)
    } catch (error) {
      console.error('Erro ao salvar:', error)
    } finally {
      setIsSaving(false)
    }
  }

  const handleCancel = () => {
    setEditedVehicle(vehicle)
    setIsEditMode(false)
  }

  const renderTabContent = () => {
    const props = { vehicle: editedVehicle, isEditMode, onEditChange: handleEditChange }
    
    switch (activeTab) {
      case 'gerais':
        return <VehicleGeneralTab {...props} />
      case 'frota':
        return <VehicleFleetTab {...props} />
      case 'tecnico':
        return <VehicleTechnicalTab {...props} />
      case 'administrativa':
        return <VehicleAdministrativeTab {...props} />
      case 'operacional':
        return <VehicleOperationalTab {...props} />
      case 'documentacao':
        return <VehicleDocumentationTab {...props} />
      case 'arquivos':
        return <VehicleFilesTab {...props} />
      default:
        return null
    }
  }

  // Mapeamento de ícones para tabs
  const tabIcons = {
    gerais: <FileText size={18} />,
    frota: <Truck size={18} />,
    tecnico: <Wrench size={18} />,
    administrativa: <File size={18} />,
    operacional: <Coins size={18} />,
    documentacao: <Disc3 size={18} />,
    arquivos: <History size={18} />,
  }

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      {/* Modal Background: Branco limpo */}
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-5xl overflow-hidden flex flex-col" style={{ backgroundColor: '#FFFFFF', height: '92vh' }}>
        
        {/* ===== HEADER PRINCIPAL ===== */}
        <div className="border-b border-gray-200 px-6 py-4 bg-white">
          <div className="flex items-center justify-between gap-4">
            {/* Esquerda: Botão voltar + Placa */}
            <div className="flex items-center gap-4 flex-shrink-0">
              <button
                onClick={onClose}
                className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
                title="Voltar"
              >
                <ArrowLeft size={22} style={{ color: '#6B7280' }} />
              </button>
              <div>
                <h2 className="text-2xl font-bold font-mono mt-0.5" style={{ color: '#111827' }}>{editedVehicle.placa}</h2>
              </div>
            </div>

            {/* Centro: Badges de informação rápida (4 blocos) */}
            <div className="flex items-center gap-3 flex-1 px-4">
              {/* Marca */}
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg" style={{ backgroundColor: '#FFFFFF' }}>
                <Shield size={18} style={{ color: '#6B7280' }} />
                <div className="min-w-0">
                  <p className="text-sm font-semibold truncate" style={{ color: '#111827' }}>{editedVehicle.marca?.nome || '—'}</p>
                </div>
              </div>

              {/* Modelo */}
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg" style={{ backgroundColor: '#FFFFFF' }}>
                <Car size={18} style={{ color: '#6B7280' }} />
                <div className="min-w-0">
                  <p className="text-sm font-semibold truncate" style={{ color: '#111827' }}>{editedVehicle.modelo?.nome || '—'}</p>
                </div>
              </div>

              {/* Combustível */}
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg" style={{ backgroundColor: '#FFFFFF' }}>
                <Fuel size={18} style={{ color: '#6B7280' }} />
                <div className="min-w-0">
                  <p className="text-sm font-semibold truncate" style={{ color: '#111827' }}>{editedVehicle.combustivel || '—'}</p>
                </div>
              </div>

              {/* Ano */}
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg" style={{ backgroundColor: '#FFFFFF' }}>
                <Calendar size={18} style={{ color: '#6B7280' }} />
                <div className="min-w-0">
                  <p className="text-sm font-semibold" style={{ color: '#111827' }}>{editedVehicle.ano_fabricacao || '—'}</p>
                </div>
              </div>
            </div>

            {/* Direita: Status Badge + Botões */}
            <div className="flex items-center gap-3 flex-shrink-0">
              {/* Badge Status com bolinha verde */}
              <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-full" style={{ backgroundColor: '#DCFCE7' }}>
                <span className="w-2 h-2 rounded-full" style={{ backgroundColor: '#15803D' }}></span>
                <span className="text-sm font-medium" style={{ color: '#15803D' }}>Ativo</span>
              </div>

              {/* Botão Editar */}
              {!isEditMode ? (
                <button
                  onClick={() => setIsEditMode(true)}
                  className="flex items-center gap-2 px-3 py-1.5 text-white rounded-lg font-medium text-sm hover:opacity-90 transition-opacity"
                  style={{ backgroundColor: '#0046E4' }}
                >
                  <Pencil size={16} />
                  Editar
                </button>
              ) : (
                <div className="flex gap-2">
                  <button
                    onClick={handleSave}
                    disabled={isSaving}
                    className="flex items-center gap-2 px-3 py-1.5 text-white rounded-lg font-medium text-sm disabled:opacity-50"
                    style={{ backgroundColor: '#15803D' }}
                  >
                    <Save size={16} />
                    Salvar
                  </button>
                  <button
                    onClick={handleCancel}
                    className="flex items-center gap-2 px-3 py-1.5 rounded-lg font-medium text-sm"
                    style={{ backgroundColor: '#E5E7EB', color: '#111827' }}
                  >
                    Cancelar
                  </button>
                </div>
              )}

              {/* Botão Mais Opções */}
              <button className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors" title="Mais opções">
                <MoreVertical size={20} style={{ color: '#6B7280' }} />
              </button>

              {/* Botão Fechar */}
              <button
                onClick={onClose}
                className="p-1.5 hover:bg-gray-100 rounded-lg transition-colors"
                title="Fechar"
              >
                <X size={20} style={{ color: '#6B7280' }} />
              </button>
            </div>
          </div>
        </div>

        {/* ===== BARRA DE TABS ===== */}
        <div className="border-b border-gray-200 px-6 overflow-hidden" style={{ backgroundColor: '#FFFFFF' }}>
          <div className="flex gap-6 py-0">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className="flex items-center gap-2 px-0 py-3 font-medium text-sm whitespace-nowrap border-b-2 transition-all"
                style={{
                  color: activeTab === tab.id ? '#0046E4' : '#6B7280',
                  borderBottomColor: activeTab === tab.id ? '#0046E4' : 'transparent',
                }}
              >
                {tabIcons[tab.id as TabType]}
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* ===== CONTEÚDO PRINCIPAL (2 COLUNAS) ===== */}
        <div className="flex flex-1 overflow-hidden" style={{ backgroundColor: '#FFFFFF' }}>
          
          {/* COLUNA ESQUERDA (~35%) - Foto + Resumo */}
          <div className="w-1/3 flex flex-col gap-2 p-3 border-r border-gray-200 overflow-hidden" style={{ backgroundColor: '#FFFFFF' }}>
            
            {/* PARTE SUPERIOR - Foto com moldura */}
            <div className="flex flex-col gap-2 flex-shrink-0">
              {/* Card da Imagem com moldura */}
              <div className="rounded-lg shadow-md overflow-hidden border border-gray-200 flex items-center justify-center" style={{ backgroundColor: '#FFFFFF', height: '180px' }}>
                {editedVehicle.foto ? (
                  <img
                    src={editedVehicle.foto}
                    alt={editedVehicle.placa}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="text-center">
                    <div className="text-6xl mb-3" style={{ opacity: 0.2 }}>🚗</div>
                    <p className="text-sm" style={{ color: '#6B7280' }}>Nenhuma imagem</p>
                  </div>
                )}
              </div>

              {/* Botão Alterar Foto */}
              {isEditMode && (
                <button className="flex items-center justify-center gap-2 px-3 py-2 rounded-lg border-2 font-medium text-sm transition-colors" style={{ borderColor: '#0046E4', color: '#0046E4' }}>
                  <Camera size={16} />
                  Alterar foto
                </button>
              )}
            </div>

            {/* PARTE INFERIOR - Resumo com linhas */}
            <div className="flex-1 flex flex-col gap-1 overflow-y-auto min-h-0">
              {/* Card Resumo */}
              <div className="bg-white rounded-lg border border-gray-100 p-2">
                <h4 className="font-bold text-xs mb-2 px-1" style={{ color: '#111827' }}>Resumo</h4>
                <div className="space-y-0 divide-y divide-gray-100">
                  <div className="flex items-center justify-between py-1.5 px-1">
                    <div className="flex items-center gap-1.5">
                      <Shield size={12} style={{ color: '#6B7280' }} />
                      <span className="text-xs" style={{ color: '#6B7280' }}>Marca</span>
                    </div>
                    <span className="text-xs font-semibold" style={{ color: '#111827' }}>{editedVehicle.marca?.nome || '—'}</span>
                  </div>
                  <div className="flex items-center justify-between py-1.5 px-1">
                    <div className="flex items-center gap-1.5">
                      <Car size={12} style={{ color: '#6B7280' }} />
                      <span className="text-xs" style={{ color: '#6B7280' }}>Modelo</span>
                    </div>
                    <span className="text-xs font-semibold" style={{ color: '#111827' }}>{editedVehicle.modelo?.nome || '—'}</span>
                  </div>
                  <div className="flex items-center justify-between py-1.5 px-1">
                    <div className="flex items-center gap-1.5">
                      <Calendar size={12} style={{ color: '#6B7280' }} />
                      <span className="text-xs" style={{ color: '#6B7280' }}>Ano</span>
                    </div>
                    <span className="text-xs font-semibold" style={{ color: '#111827' }}>{editedVehicle.ano_fabricacao || '—'}</span>
                  </div>
                  <div className="flex items-center justify-between py-1.5 px-1">
                    <div className="flex items-center gap-1.5">
                      <Fuel size={12} style={{ color: '#6B7280' }} />
                      <span className="text-xs" style={{ color: '#6B7280' }}>Combustível</span>
                    </div>
                    <span className="text-xs font-semibold" style={{ color: '#111827' }}>{editedVehicle.combustivel || '—'}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* COLUNA DIREITA (65%) - Detalhes + KPIs */}
          <div className="flex-1 flex flex-col gap-2 p-3 overflow-hidden">
            
            {/* Se for tab "Dados Gerais", mostrar layout especial com KPIs */}
            {activeTab === 'gerais' ? (
              <>
                {/* Card de Informações do Veículo em 2 colunas */}
                <div className="bg-white rounded-lg p-2 flex-shrink-0 border border-gray-100">
                  <h3 className="font-bold text-sm mb-2 px-1" style={{ color: '#111827' }}>Informações</h3>
                  <div className="grid grid-cols-2 gap-x-3 gap-y-0 divide-y divide-gray-100">
                    {[
                      { label: 'Prefixo', value: editedVehicle.prefixo, icon: FileText },
                      { label: 'Renavam', value: editedVehicle.renavam, icon: FileText },
                      { label: 'Cor', value: editedVehicle.cor, icon: Circle },
                      { label: 'Lotação', value: editedVehicle.lotacao, icon: Users },
                      { label: 'Motorização', value: editedVehicle.motorizacao, icon: Wrench },
                      { label: 'Secretaria', value: editedVehicle.secretaria, icon: Building },
                      { label: 'Chassi', value: editedVehicle.chassis, icon: Shield },
                      { label: 'Responsável', value: editedVehicle.responsavel, icon: Users },
                    ].map((field, idx) => {
                      const IconComponent = field.icon
                      return (
                        <div key={idx} className="flex items-center justify-between py-1.5 px-1">
                          <div className="flex items-center gap-1.5 min-w-0">
                            <IconComponent size={12} style={{ color: '#6B7280', flexShrink: 0 }} />
                            <span className="text-xs" style={{ color: '#6B7280' }}>{field.label}</span>
                          </div>
                          <span className="text-xs font-semibold ml-2" style={{ color: '#111827' }}>{field.value || '—'}</span>
                        </div>
                      )
                    })}
                  </div>
                </div>

                {/* Linha de KPIs (5 mini-cards) - SEM SCROLL */}
                <div className="grid grid-cols-5 gap-1.5 flex-shrink-0">
                  <KPICard icon={<Wrench size={16} style={{ color: '#3B82F6' }} />} label="Manutenções" value="3" subtitle="Este ano" color="#3B82F6" />
                  <KPICard icon={<Fuel size={16} style={{ color: '#10B981' }} />} label="Abastecimentos" value="8" subtitle="Este ano" color="#10B981" />
                  <KPICard icon={<AlertCircle size={16} style={{ color: '#F59E0B' }} />} label="Multas" value="0" subtitle="Ativas" color="#F59E0B" />
                  <KPICard icon={<Coins size={16} style={{ color: '#8B5CF6' }} />} label="Gastos (ano)" value="R$ 8.520" subtitle="Total" color="#8B5CF6" />
                  <KPICard icon={<Gauge size={16} style={{ color: '#06B6D4' }} />} label="Quilometragem" value="18.240 km" subtitle="Atual" color="#06B6D4" />
                </div>

                {/* Card de Observações */}
                <div className="bg-white rounded-lg p-2.5 flex-1 min-h-0 overflow-y-auto border border-gray-100">
                  <h3 className="font-bold text-sm mb-2" style={{ color: '#111827' }}>Observações</h3>
                  <p className="text-xs leading-relaxed" style={{ color: '#6B7280' }}>
                    {editedVehicle.observacoes || 'Nenhuma observação registrada para este veículo.'}
                  </p>
                </div>
              </>
            ) : (
              /* Renderizar componentes das outras abas - SEM SCROLL */
              <div className="bg-white rounded-lg p-3 flex-1 overflow-y-auto">
                {renderTabContent()}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

// Componente KPI Card
interface KPICardProps {
  icon: React.ReactNode
  label: string
  value: string
  subtitle: string
  color: string
}

function KPICard({ icon, label, value, subtitle, color }: KPICardProps) {
  return (
    <div className="bg-white rounded-lg p-2 flex flex-col items-center text-center border border-gray-100">
      <div className="w-8 h-8 flex items-center justify-center rounded-full mx-auto mb-1" style={{ backgroundColor: `${color}20` }}>
        {icon}
      </div>
      <p className="text-xs font-medium mb-0.5" style={{ color: '#6B7280' }}>
        {label}
      </p>
      <p className="text-sm font-bold" style={{ color: '#111827' }}>
        {value}
      </p>
      <p className="text-xs mt-0.5" style={{ color: '#9CA3AF' }}>
        {subtitle}
      </p>
    </div>
  )
}
