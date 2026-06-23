// ── Auth ───────────────────────────────────────────────────────────────────────

export interface LoginRequest {
  username: string
  password: string
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface Usuario {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  perfil: Perfil
  secretaria_id: number | null
  secretaria: Secretaria | null
  telefone: string
  foto: string | null
  ativo: boolean
  is_superuser: boolean
}

export type Perfil = 'ADMIN' | 'GESTOR' | 'OPERADOR' | 'OFICINA' | 'AUDITOR'

export interface Secretaria {
  id: number
  nome: string
  sigla: string
  ativa: boolean
}

// ── Veículos ───────────────────────────────────────────────────────────────────

// ── Parametrizadores ──────────────────────────────────────────────────────────

export interface Categoria {
  id: number
  nome: string
  ativo: boolean
}

export interface TipoFrota {
  id: number
  nome: string
  ativo: boolean
}

export interface Unidade {
  id: number
  nome: string
  secretaria_id: number | null
  ativa: boolean
}

export interface Subunidade {
  id: number
  nome: string
  unidade_id: number | null
  ativa: boolean
}

export interface CentroCusto {
  id: number
  codigo: string
  descricao: string
  ativo: boolean
}

// ── Marca, Modelo, TipoVeiculo ────────────────────────────────────────────────

export interface Marca {
  id: number
  nome: string
  ativo: boolean
}

export interface Modelo {
  id: number
  nome: string
  marca_id: number
  tipo_veiculo_id: number | null
  ativo: boolean
}

export interface TipoVeiculo {
  id: number
  nome: string
  ativo: boolean
}

// ── Situação e Combustível ────────────────────────────────────────────────────

export type SituacaoVeiculo = 'ATIVA' | 'INATIVA' | 'MANUTENCAO'
export type StatusVeiculo = 'ATIVO' | 'INATIVO' | 'BAIXADO' | 'LEILOADO'

export type TipoControle = 'QUILOMETRAGEM' | 'HORIMETRO'
export type Combustivel = 'GASOLINA' | 'DIESEL' | 'FLEX' | 'ELETRICO' | 'GNV'
export type TipoVeiculoNome = 'AUTOMOVEL' | 'UTILITARIO' | 'CAMIONETE' | 'CAMIONETA' | 'MICRO_ONIBUS' | 'ONIBUS' | 'MOTOCICLETA' | 'CAMINHAO' | 'CAMINHAO_BASCULANTE' | 'CAMINHAO_PIPA' | 'CAMINHAO_VARREDOR' | 'RETROESCAVADEIRA' | 'PA_CARREGADEIRA' | 'TRATOR_AGRICOLA' | 'AMBULANCIA' | 'VIATURA_GUARDA_MUNICIPAL' | 'ONIBUS_ESCOLAR' | 'VAN'

// ── Veículos ───────────────────────────────────────────────────────────────────

export interface VeiculoListItem {
  id: number
  placa: string
  prefixo: string
  marca: Marca | null
  modelo: Modelo | null
  ano_fabricacao: number
  situacao: SituacaoVeiculo
  categoria: Categoria | null
  combustivel: Combustivel
}

export interface Veiculo extends VeiculoListItem {
  // 4.2.1 DADOS GERAIS
  chassi: string
  renavam: string
  ano_modelo: number | null
  cor: string
  motorizacao: string
  observacoes: string
  status: StatusVeiculo
  tipo_veiculo_nome: TipoVeiculoNome
  
  // 4.2.2 CLASSIFICAÇÃO
  tipo_frota_id?: number | null
  categoria_id?: number | null
  numero_patrimonio: string | null
  valor_aquisicao: number | null
  tipo_aquisicao: 'COMPRADO' | 'DOADO' | null
  tipo_convenio: 'PM' | 'BOMBEIROS' | null
  nome_locador: string | null
  valor_locacao: number | null
  
  // 4.2.3 ADMINISTRATIVA
  secretaria_id: number | null
  unidade: Unidade | null
  unidade_id?: number | null
  subunidade: Subunidade | null
  subunidade_id?: number | null
  centro_custo: CentroCusto | null
  centro_custo_id?: number | null
  
  // 4.2.4 OPERACIONAL
  tipo_veiculo: TipoVeiculo | null
  tipo_registro_id?: number | null
  tipo_controle: TipoControle
  hodometro_horimetro_inicial: number
  capacidade_tanque: number | null
  capacidade_passageiros: number | null
  capacidade_carga: number | null
  
  // 4.2.5 DADOS TÉCNICOS
  cilindrada: number | null
  potencia: number | null
  transmissao: string | null
  tracao: string | null
  vidros_eletricos: boolean | null
  direcao: string | null
  ar_condicionado: boolean | null
  pneu_dimensao: string | null
  pneu_velocidade: string | null
  pneu_carga: string | null
  
  // 4.2.6 DOCUMENTAÇÃO
  vencimento_licenciamento: string | null
  vencimento_seguro: string | null
  vencimento_ipva: string | null
  
  // 4.2.7 LOCALIZAÇÃO
  uf: string
  municipio: string
  
  // IDs para relações
  marca_id?: number | null
  modelo_id?: number | null
}

// ── Condutores ────────────────────────────────────────────────────────────────

export type StatusCondutor = 'ATIVO' | 'INATIVO' | 'SUSPENSO'

export interface CondutorListItem {
  id: number
  prontuario: string
  nome: string
  cpf: string
  cargo: string
  secretaria_id: number
  status: StatusCondutor
  cnh_categoria: string
  cnh_vencimento: string | null
}

export interface Condutor extends CondutorListItem {
  data_nascimento: string
  rg: string
  orgao_emissor: string
  endereco: string
  telefone: string
  email: string
  unidade: string
  cnh_numero: string
  cnh_emissao: string | null
  cnh_orgao: string
  foto: string | null
  cnh_arquivo: string | null
}

// ── Manutenção (SMV) ──────────────────────────────────────────────────────────

export type EtapaSMV =
  | 'SOLICITACAO'
  | 'RECEPCAO'
  | 'DIAGNOSTICO'
  | 'ORCAMENTO'
  | 'APROVACAO'
  | 'EXECUCAO'
  | 'RETIRADA'
  | 'EMISSAO_NF'
  | 'FINALIZADO'

export type UrgenciaSMV = 'BAIXA' | 'MEDIA' | 'ALTA'

export interface SMVListItem {
  id: number
  numero: string
  veiculo_id: number
  etapa: EtapaSMV
  urgencia: UrgenciaSMV
  dt_solicitacao: string
  msgs_nao_lidas: number
}

export interface SMV extends SMVListItem {
  solicitante_id: number
  descricao_problema: string
  km_entrada: number | null
  km_saida: number | null
  diagnostico: string
  observacoes: string
  dt_recepcao: string | null
  dt_diagnostico: string | null
  dt_inicio_exec: string | null
  dt_retirada: string | null
  dt_finalizacao: string | null
}

// ── Multas ────────────────────────────────────────────────────────────────────

export type StatusMulta = 'PENDENTE' | 'PAGA' | 'CONTESTADA' | 'VENCIDA'

export interface MultaListItem {
  id: number
  placa: string
  data_infracao: string
  valor: string
  status: StatusMulta
  pontos: number
  data_vencimento: string
}

export interface Multa extends MultaListItem {
  condutor_id: number | null
  tipo_infracao_id: number | null
  prazo_indicacao: string | null
  prazo_defesa: string | null
  observacao: string
  arquivo: string | null
}

// ── Paginação ─────────────────────────────────────────────────────────────────

export interface PaginatedResponse<T> {
  total: number
  page: number
  page_size: number
  items: T[]
}
