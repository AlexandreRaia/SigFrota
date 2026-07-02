/**
 * TIPOS E INTERFACES PARA O MODAL
 * 
 * Se seus tipos em @/types não incluem todos estes campos,
 * você pode usar estas interfaces estendidas
 */

// Se você precisa estender a interface Veiculo existente
export interface VeiculoCompleto {
  // Identificação
  id: number
  placa: string
  prefixo?: string
  chassi: string
  renavam: string
  numero_patrimonio?: string

  // Classificação
  marca?: { id: number; nome: string }
  modelo?: { id: number; nome: string }
  tipo_veiculo?: { id: number; nome: string }
  categoria?: { id: number; nome: string }
  tipo_frota?: { id: number; nome: string }

  // Especificações
  ano_fabricacao: number
  ano_modelo: number
  cor?: string
  combustivel?: string
  motorizacao?: string
  cilindrada?: number
  potencia?: number
  transmissao?: string
  tracao?: string
  
  // Conforto
  vidros_eletricos?: boolean
  direcao?: boolean
  ar_condicionado?: boolean

  // Pneus
  pneu_dimensao?: string
  pneu_velocidade?: string
  pneu_carga?: string
  capacidade_tanque?: number

  // Operacional
  situacao: 'Ativo' | 'Inativo' | 'Manutenção'
  hodometro_horimetro_inicial?: number
  tipo_controle?: 'QUILOMETRAGEM' | 'HORIMETRO'
  capacidade_passageiros?: number
  capacidade_carga?: number

  // Alocação
  secretaria?: { id: number; nome: string }
  unidade?: { id: number; nome: string }
  subunidade?: { id: number; nome: string }
  centro_custo?: { id: number; nome: string }

  // Administrativo
  valor_aquisicao?: number
  tipo_aquisicao?: 'Proprio' | 'Leasing' | 'Comodato'
  tipo_convenio?: string
  nome_locador?: string
  valor_locacao?: number

  // Documentação
  vencimento_licenciamento?: string // ISO date
  vencimento_seguro?: string // ISO date
  vencimento_ipva?: string // ISO date

  // Mídia
  foto?: string // URL

  // Observações
  observacoes?: string

  // Auditoria
  criado_em?: string // ISO date
  atualizado_em?: string // ISO date
}

// Response type para listagem de veículos
export interface VeiculoListItem {
  id: number
  placa: string
  prefixo?: string
  marca: { nome: string }
  modelo: { nome: string }
  ano_fabricacao: number
  situacao: string
}

// Request type para atualização
export interface UpdateVeiculoRequest {
  placa?: string
  prefixo?: string
  cor?: string
  combustivel?: string
  motorizacao?: string
  situacao?: string
  hodometro_horimetro_inicial?: number
  [key: string]: any // Aceita qualquer campo
}

// Modal state type
export interface VehicleModalState {
  isOpen: boolean
  vehicle: VeiculoCompleto | null
  isEditMode: boolean
  isSaving: boolean
  error?: string
}

// Tab type
export type VehicleTabType = 
  | 'gerais' 
  | 'frota' 
  | 'tecnico' 
  | 'administrativa' 
  | 'operacional' 
  | 'documentacao' 
  | 'arquivos'

// Props comuns para componentes de aba
export interface TabComponentProps {
  vehicle: VeiculoCompleto
  isEditMode: boolean
  onEditChange: (field: string, value: any) => void
}

// Status de vencimento
export enum VencimentoStatus {
  VENCIDO = 'vencido',
  PROXIMO = 'proximo', // < 30 dias
  VALIDO = 'valido',
  NAO_INFORMADO = 'nao_informado'
}

// Função helper para determinar status de vencimento
export function getVencimentoStatus(date: string | null | undefined): VencimentoStatus {
  if (!date) return VencimentoStatus.NAO_INFORMADO
  
  const daysUntil = Math.ceil((new Date(date).getTime() - new Date().getTime()) / (1000 * 60 * 60 * 24))
  
  if (daysUntil < 0) return VencimentoStatus.VENCIDO
  if (daysUntil < 30) return VencimentoStatus.PROXIMO
  return VencimentoStatus.VALIDO
}

// Cores para status
export const VencimentoStatusColors = {
  [VencimentoStatus.VENCIDO]: 'bg-red-500/20 text-red-600 border-red-500/30',
  [VencimentoStatus.PROXIMO]: 'bg-yellow-500/20 text-yellow-600 border-yellow-500/30',
  [VencimentoStatus.VALIDO]: 'bg-emerald-500/20 text-emerald-600 border-emerald-500/30',
  [VencimentoStatus.NAO_INFORMADO]: 'bg-gray-500/20 text-gray-600 border-gray-500/30',
}

// Função helper para cores
export function getVencimentoColor(date: string | null | undefined): string {
  return VencimentoStatusColors[getVencimentoStatus(date)]
}
