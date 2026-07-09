'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { veiculoService } from '@/services/veiculos'
import { Button } from '@/components/ui/Button'
import type { Veiculo, VeiculoListItem } from '@/types'
import { FiFileText, FiEdit2, FiPower } from 'react-icons/fi'

const TABS = [
  { id: 'gerais', label: 'Dados Gerais' },
  { id: 'classificacao', label: 'Frota' },
  { id: 'tecnico', label: 'Técnico' },
  { id: 'operacional', label: 'Operação' },
  { id: 'documentacao', label: 'Documentação' },
]

// Funções de máscara
const formatPlaca = (value: string): string => {
  const cleaned = value.toUpperCase().replace(/[^A-Z0-9]/g, '')
  if (cleaned.length === 0) return ''
  
  // Detecta Mercosul (AA-9-AA-9999) ou antigo (AAA-9999)
  if (cleaned.length >= 4) {
    if (/^[A-Z]{2}\d[A-Z]{2}\d{4}$/.test(cleaned) || cleaned.length >= 8) {
      // Mercosul: AA-9-AA-9999
      const match = cleaned.match(/^([A-Z]{2})(\d)([A-Z]{2})(\d{4})/)
      if (match) return `${match[1]}-${match[2]}-${match[3]}-${match[4]}`.slice(0, 12)
    } else {
      // Antigo: AAA-9999
      const match = cleaned.match(/^([A-Z]{3})(\d{4})/)
      if (match) return `${match[1]}-${match[2]}`.slice(0, 8)
    }
  }
  return cleaned.slice(0, 8)
}

const formatRenavam = (value: string): string => {
  return value.replace(/\D/g, '').slice(0, 11)
}

const formatChassi = (value: string): string => {
  return value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 17)
}

// ── Helpers ──────────────────────────────────────────────────────────────────

const InfoRow = ({
  label,
  value,
  mono = false,
}: {
  label: string
  value: string | number | null | undefined
  mono?: boolean
}) => (
  <div className="flex justify-between items-baseline gap-2 py-1.5 border-b border-gray-50 last:border-0">
    <span className="text-xs text-gray-500 font-medium shrink-0">{label}</span>
    <span className={`text-sm text-gray-800 text-right truncate ${mono ? 'font-mono text-xs' : ''}`}>
      {value != null && value !== '' ? String(value) : <span className="text-gray-300">—</span>}
    </span>
  </div>
)

const fmtDate = (v: string | null | undefined) =>
  v ? new Date(v).toLocaleDateString('pt-BR') : null

// Situação do veículo (tolerante a ATIVO/ATIVA por compatibilidade)
const isAtivo = (s?: string | null) => s === 'ATIVA' || s === 'ATIVO'

const situacaoBadge = (s?: string | null): { cls: string; label: string } => {
  const map: Record<string, { cls: string; label: string }> = {
    ATIVA: { cls: 'bg-green-100 text-green-700', label: 'Ativa' },
    ATIVO: { cls: 'bg-green-100 text-green-700', label: 'Ativa' },
    INATIVA: { cls: 'bg-red-100 text-red-700', label: 'Inativa' },
    INATIVO: { cls: 'bg-red-100 text-red-700', label: 'Inativa' },
    MANUTENCAO: { cls: 'bg-amber-100 text-amber-700', label: 'Manutenção' },
  }
  return map[s ?? ''] ?? { cls: 'bg-gray-100 text-gray-700', label: s ?? '—' }
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function Veiculos() {
  const [q, setQ] = useState('')
  const [situacao, setSituacao] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [activeTab, setActiveTab] = useState('gerais')
  const [editing, setEditing] = useState<Veiculo | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)
  const [showDetail, setShowDetail] = useState(false)
  const [detailVeiculo, setDetailVeiculo] = useState<Veiculo | null>(null)
  const [loadingDetail, setLoadingDetail] = useState(false)

  // Queries
  const { data: veiculos, isLoading } = useQuery({
    queryKey: ['veiculos', { q, situacao }],
    queryFn: () => veiculoService.listar({ q, situacao }),
  })

  const { data: tiposFrota } = useQuery({
    queryKey: ['veiculos', 'tiposFrota'],
    queryFn: () => veiculoService.tiposFrota(),
  })

  const { data: marcas } = useQuery({
    queryKey: ['veiculos', 'marcas'],
    queryFn: () => veiculoService.marcas(),
  })

  const [form, setForm] = useState<Partial<Veiculo>>({
    placa: '',
    prefixo: '',
    chassi: '',
    renavam: '',
    ano_fabricacao: new Date().getFullYear(),
    combustivel: 'FLEX',
    tipo_registro_id: 1,  // Veículo por padrão
    uf: 'SP',
    situacao: 'ATIVA',
    tipo_controle: 'QUILOMETRAGEM',
    hodometro_horimetro_inicial: 0,
    tipo_convenio: null,
  })

  const [marcaId, setMarcaId] = useState<number | null>(null)
  const { data: modelos } = useQuery({
    queryKey: ['veiculos', 'modelos', marcaId],
    queryFn: () => marcaId ? veiculoService.modelos(marcaId) : Promise.resolve([]),
    enabled: !!marcaId,
  })

  // Cascata Administrativa
  const [unidadeId, setUnidadeId] = useState<number | null>(null)
  const { data: unidades } = useQuery({
    queryKey: ['veiculos', 'unidades'],
    queryFn: () => veiculoService.unidades(),
  })

  const { data: subunidades } = useQuery({
    queryKey: ['veiculos', 'subunidades', unidadeId],
    queryFn: () => unidadeId ? veiculoService.subunidades(unidadeId) : Promise.resolve([]),
    enabled: !!unidadeId,
  })

  const { data: centrosCusto } = useQuery({
    queryKey: ['veiculos', 'centrosCusto'],
    queryFn: () => veiculoService.centrosCusto(),
  })

  const queryClient = useQueryClient()

  const createMutation = useMutation<Veiculo, Error, Partial<Veiculo>>({
    mutationFn: (data) => veiculoService.criar(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['veiculos'] })
      setSuccessMessage('Veículo criado com sucesso!')
      setTimeout(() => setShowForm(false), 1000)
    },
  })

  const updateMutation = useMutation<Veiculo, Error, { id: number; data: Partial<Veiculo> }>({
    mutationFn: ({ id, data }) => veiculoService.atualizar(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['veiculos'] })
      setSuccessMessage('Veículo atualizado com sucesso!')
      setTimeout(() => setShowForm(false), 1000)
    },
  })

  const deleteMutation = useMutation<void, Error, number>({
    mutationFn: (id) => veiculoService.excluir(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['veiculos'] })
      setSuccessMessage('Veículo excluído com sucesso!')
    },
  })

  const toggleStatusMutation = useMutation<Veiculo, Error, VeiculoListItem>({
    mutationFn: (v) => {
      return isAtivo(v.situacao) ? veiculoService.inativar(v.id) : veiculoService.ativar(v.id)
    },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['veiculos'] }),
  })

  function openCreate() {
    setEditing(null)
    setForm({
      placa: '',
      prefixo: '',
      chassi: '',
      renavam: '',
      ano_fabricacao: new Date().getFullYear(),
      combustivel: 'FLEX',
      tipo_registro_id: 1,  // Veículo por padrão
      uf: 'SP',
      situacao: 'ATIVA',
      tipo_controle: 'QUILOMETRAGEM',
      hodometro_horimetro_inicial: 0,
      tipo_convenio: null,
      // Dados Técnicos
      cilindrada: undefined,
      potencia: undefined,
      transmissao: '',
      tracao: '',
      vidros_eletricos: false,
      direcao: '',
      ar_condicionado: false,
      pneu_dimensao: '',
      pneu_velocidade: '',
      pneu_carga: '',
      // Documentação
      vencimento_ipva: undefined,
    })
    setMarcaId(null)
    setUnidadeId(null)
    setActiveTab('gerais')
    setShowForm(true)
  }

  async function openEdit(v: VeiculoListItem) {
    const full = await veiculoService.detalhe(v.id)
    setEditing(full)
    setForm(full)
    setMarcaId(full.marca?.id || null)
    setUnidadeId(full.unidade_id ?? null)
    setActiveTab('gerais')
    setShowForm(true)
  }

  async function handleSave() {
    setFormError(null)

    // Validar campos obrigatórios
    if (!form.placa?.trim()) {
      setFormError('Placa é obrigatória')
      return
    }
    if (!form.prefixo?.trim()) {
      setFormError('Prefixo é obrigatório')
      return
    }
    if (!form.chassi?.trim() || form.chassi.length !== 17) {
      setFormError('Chassi deve ter exatamente 17 caracteres')
      return
    }
    if (!form.renavam?.trim() || !/^\d{11}$/.test(form.renavam)) {
      setFormError('RENAVAM deve ter exatamente 11 dígitos')
      return
    }
    if (!marcaId) {
      setFormError('Marca é obrigatória')
      return
    }
    if (!form.modelo_id) {
      setFormError('Modelo é obrigatório')
      return
    }
    if (!form.tipo_registro_id) {
      setFormError('Tipo de Registro é obrigatório')
      return
    }

    try {
      // Preparar dados para envio
      const payload = {
        ...form,
        marca_id: marcaId,
      }
      
      if (editing) {
        await updateMutation.mutateAsync({ id: editing.id, data: payload })
      } else {
        await createMutation.mutateAsync(payload)
      }
    } catch (err: any) {
      setFormError(err?.response?.data?.detail || err?.message || 'Erro ao salvar veículo')
    }
  }

  async function handleDelete(id: number) {
    if (!window.confirm('Tem certeza que deseja excluir este veículo?')) return
    try {
      await deleteMutation.mutateAsync(id)
    } catch (err: any) {
      setFormError(err?.response?.data?.detail || 'Erro ao excluir')
    }
  }

  async function handleView(v: VeiculoListItem) {
    setLoadingDetail(true)
    setDetailVeiculo(null)
    setActiveTab('gerais')
    setShowDetail(true)
    try {
      const full = await veiculoService.detalhe(v.id)
      setDetailVeiculo(full)
    } finally {
      setLoadingDetail(false)
    }
  }

  return (
    <div className="space-y-4 p-6">
      {/* Cabeçalho */}
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">🚗 Veículos</h1>
        <Button onClick={openCreate} className="bg-blue-600 hover:bg-blue-700">
          + Novo Veículo
        </Button>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow p-4 flex gap-4">
        <input
          type="text"
          placeholder="🔍 Buscar por placa, prefixo..."
          className="px-4 py-2 border rounded-lg flex-1"
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <select
          className="px-4 py-2 border rounded-lg"
          value={situacao}
          onChange={(e) => setSituacao(e.target.value)}
        >
          <option value="">Todas as situações</option>
          <option value="ATIVA">Ativa</option>
          <option value="INATIVA">Inativa</option>
          <option value="MANUTENCAO">Manutenção</option>
        </select>
      </div>

      {/* Tabela */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700">Placa</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700">Marca / Modelo</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700">Ano</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700">Combustível</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700">Unidade</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700">Situação</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {isLoading ? (
              <tr>
                <td colSpan={7} className="px-6 py-10 text-center text-gray-400">Carregando...</td>
              </tr>
            ) : veiculos?.length === 0 ? (
              <tr>
                <td colSpan={7} className="px-6 py-10 text-center text-gray-400">Nenhum veículo encontrado</td>
              </tr>
            ) : (
              veiculos?.map((v) => (
                <tr key={v.id} className="hover:bg-gray-50">
                  <td className="px-6 py-3 font-mono font-bold text-gray-900">{v.placa}</td>
                  <td className="px-6 py-3 text-gray-600">{v.marca?.nome} {v.modelo?.nome}</td>
                  <td className="px-6 py-3 text-gray-600">{v.ano_fabricacao}</td>
                  <td className="px-6 py-3 text-gray-600">{v.combustivel}</td>
                  <td className="px-6 py-3 text-gray-600">{v.unidade?.nome ?? <span className="text-gray-300">—</span>}</td>
                  <td className="px-6 py-3">
                    {(() => {
                      const b = situacaoBadge(v.situacao)
                      return (
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${b.cls}`}>
                          {b.label}
                        </span>
                      )
                    })()}
                  </td>
                  <td className="px-6 py-3">
                    <div className="flex items-center gap-0.5">
                      <button
                        title="Ver ficha"
                        onClick={() => handleView(v)}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      >
                        <FiFileText size={16} />
                      </button>
                      <button
                        title="Editar"
                        onClick={() => openEdit(v)}
                        className="p-2 text-gray-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-colors"
                      >
                        <FiEdit2 size={16} />
                      </button>
                      <button
                        title={
                          isAtivo(v.situacao)
                            ? 'Inativar veículo'
                            : 'Ativar veículo'
                        }
                        onClick={() => toggleStatusMutation.mutate(v)}
                        disabled={toggleStatusMutation.isPending}
                        className={`p-2 rounded-lg transition-colors disabled:opacity-40 ${
                          isAtivo(v.situacao)
                            ? 'text-green-500 hover:text-red-600 hover:bg-red-50'
                            : 'text-gray-400 hover:text-green-600 hover:bg-green-50'
                        }`}
                      >
                        <FiPower size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Form Modal com Abas */}
      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl h-[90vh] flex flex-col overflow-hidden">
            {/* Header */}
            <div className="border-b px-6 py-4 flex justify-between items-center shrink-0">
              <h2 className="text-xl font-bold">{editing ? '✏️ Editar Veículo' : '➕ Novo Veículo'}</h2>
              <button
                onClick={() => setShowForm(false)}
                className="text-gray-500 hover:text-gray-700 text-2xl"
              >
                ✕
              </button>
            </div>

            {/* Mensagens */}
            <div className="px-6 pt-4 shrink-0">
              {successMessage && (
                <div className="mb-3 rounded-lg bg-green-50 border border-green-200 p-3 text-sm text-green-700">
                  {successMessage}
                </div>
              )}
              {formError && (
                <div className="mb-3 rounded-lg bg-red-50 border border-red-200 p-3 text-sm text-red-700">
                  {formError}
                </div>
              )}
            </div>

            {/* Tabs */}
            <div className="border-b flex gap-2 px-6 overflow-x-auto shrink-0">
              {TABS.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-4 py-3 whitespace-nowrap border-b-2 transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-600 text-blue-600 font-medium'
                      : 'border-transparent text-gray-600 hover:text-gray-900'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-6 bg-gray-50 no-scrollbar">
              {/* 📋 Dados Gerais */}
              {activeTab === 'gerais' && (
                <div className="bg-white rounded-lg p-6 space-y-4">
                  <h3 className="font-bold text-lg mb-4">Informações do Veículo</h3>
                  <div className="grid grid-cols-2 gap-4">
                    {/* Tipo de Registro e Status lado a lado */}
                    <div>
                      <label className="block text-sm font-medium mb-2">Tipo de Registro *</label>
                      <div className="flex gap-4">
                        <label className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="radio"
                            name="tipo_registro"
                            value="1"
                            checked={form.tipo_registro_id === 1}
                            onChange={(e) => setForm({ ...form, tipo_registro_id: parseInt(e.target.value) })}
                            className="w-4 h-4 cursor-pointer"
                          />
                          <span className="text-sm font-medium">🚗 Veículo</span>
                        </label>
                        <label className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="radio"
                            name="tipo_registro"
                            value="2"
                            checked={form.tipo_registro_id === 2}
                            onChange={(e) => setForm({ ...form, tipo_registro_id: parseInt(e.target.value) })}
                            className="w-4 h-4 cursor-pointer"
                          />
                          <span className="text-sm font-medium">⚙️ Máquina</span>
                        </label>
                      </div>
                    </div>

                    {/* Situação */}
                    <div>
                      <label className="block text-sm font-medium mb-1">Situação</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.situacao || 'ATIVA'}
                        onChange={(e) => setForm({ ...form, situacao: e.target.value })}
                      >
                        <option value="ATIVA">Ativa</option>
                        <option value="INATIVA">Inativa</option>
                        <option value="MANUTENCAO">Manutenção</option>
                      </select>
                    </div>

                    {/* Placa e Tipo de Veículo */}
                    <div>
                      <label className="block text-sm font-medium mb-1">Placa *</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.placa || ''}
                        onChange={(e) => setForm({ ...form, placa: formatPlaca(e.target.value) })}
                        placeholder="ABC-1234 ou AB-1-CD-1234"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Prefixo</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.prefixo || ''}
                        onChange={(e) => setForm({ ...form, prefixo: e.target.value })}
                        placeholder="V-001"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Tipo de Veículo</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.tipo_veiculo_nome || 'AUTOMOVEL'}
                        onChange={(e) => setForm({ ...form, tipo_veiculo_nome: e.target.value as any })}
                      >
                        <option value="AUTOMOVEL">Automóvel</option>
                        <option value="UTILITARIO">Utilitário</option>
                        <option value="CAMIONETE">Camionete</option>
                        <option value="CAMIONETA">Camioneta</option>
                        <option value="MICRO_ONIBUS">Micro-ônibus</option>
                        <option value="ONIBUS">Ônibus</option>
                        <option value="MOTOCICLETA">Motocicleta</option>
                        <option value="CAMINHAO">Caminhão</option>
                        <option value="CAMINHAO_BASCULANTE">Caminhão Basculante</option>
                        <option value="CAMINHAO_PIPA">Caminhão Pipa</option>
                        <option value="CAMINHAO_VARREDOR">Caminhão Varredor</option>
                        <option value="RETROESCAVADEIRA">Retroescavadeira</option>
                        <option value="PA_CARREGADEIRA">Pá Carregadeira</option>
                        <option value="TRATOR_AGRICOLA">Trator Agrícola</option>
                        <option value="AMBULANCIA">Ambulância</option>
                        <option value="VIATURA_GUARDA_MUNICIPAL">Viatura da Guarda Municipal</option>
                        <option value="ONIBUS_ESCOLAR">Ônibus Escolar</option>
                        <option value="VAN">Van</option>
                      </select>
                    </div>

                    {/* Marca e Modelo */}
                    <div>
                      <label className="block text-sm font-medium mb-1">Marca *</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={marcaId || ''}
                        onChange={(e) => {
                          const id = parseInt(e.target.value)
                          setMarcaId(id || null)
                          setForm({ ...form, marca_id: id, modelo_id: undefined })
                        }}
                      >
                        <option value="">Selecione...</option>
                        {marcas?.map((m) => (
                          <option key={m.id} value={m.id}>{m.nome}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Modelo *</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.modelo_id || ''}
                        onChange={(e) => setForm({ ...form, modelo_id: parseInt(e.target.value) || undefined })}
                        disabled={!marcaId}
                      >
                        <option value="">Selecione...</option>
                        {modelos?.map((m) => (
                          <option key={m.id} value={m.id}>{m.nome}</option>
                        ))}
                      </select>
                    </div>

                    {/* Ano Fabricação e Ano Modelo */}
                    <div>
                      <label className="block text-sm font-medium mb-1">Ano Fabricação *</label>
                      <input
                        type="number"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.ano_fabricacao || ''}
                        onChange={(e) => setForm({ ...form, ano_fabricacao: parseInt(e.target.value) })}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Ano Modelo</label>
                      <input
                        type="number"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.ano_modelo || ''}
                        onChange={(e) => setForm({ ...form, ano_modelo: e.target.value ? parseInt(e.target.value) : undefined })}
                      />
                    </div>

                    {/* Cor e Combustível */}
                    <div>
                      <label className="block text-sm font-medium mb-1">Cor</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.cor || ''}
                        onChange={(e) => setForm({ ...form, cor: e.target.value })}
                        placeholder="Ex: Branco"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Combustível</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.combustivel || ''}
                        onChange={(e) => setForm({ ...form, combustivel: e.target.value as any })}
                      >
                        <option value="FLEX">FLEX</option>
                        <option value="GASOLINA">Gasolina</option>
                        <option value="DIESEL">Diesel</option>
                        <option value="ELETRICO">Elétrico</option>
                        <option value="GNV">GNV</option>
                      </select>
                    </div>

                    {/* RENAVAM e Chassi */}
                    <div>
                      <label className="block text-sm font-medium mb-1">RENAVAM *</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.renavam || ''}
                        onChange={(e) => setForm({ ...form, renavam: formatRenavam(e.target.value) })}
                        placeholder="11 dígitos"
                        maxLength={11}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Chassi *</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.chassi || ''}
                        onChange={(e) => setForm({ ...form, chassi: formatChassi(e.target.value) })}
                        placeholder="17 caracteres"
                        maxLength={17}
                      />
                    </div>

                    {/* Observações - full width */}
                    <div className="col-span-2">
                      <label className="block text-sm font-medium mb-1">Observações</label>
                      <textarea
                        className="w-full px-3 py-2 border rounded-lg"
                        rows={2}
                        value={form.observacoes || ''}
                        onChange={(e) => setForm({ ...form, observacoes: e.target.value })}
                        placeholder="Observações adicionais..."
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* 🚗 Frota */}
              {activeTab === 'classificacao' && (
                <div className="bg-white rounded-lg p-6 space-y-4">
                  <h3 className="font-bold text-lg mb-4">Dados da Frota</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="col-span-2">
                      <label className="block text-sm font-medium mb-1">Tipo de Frota *</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg font-semibold"
                        value={form.tipo_frota_id || ''}
                        onChange={(e) => setForm({ ...form, tipo_frota_id: e.target.value ? parseInt(e.target.value) : undefined })}
                      >
                        <option value="">Selecione...</option>
                        {tiposFrota?.filter(t => t.nome !== 'CEDIDO').map((t) => (
                          <option key={t.id} value={t.id}>{t.nome}</option>
                        ))}
                      </select>
                    </div>

                    {/* Campos para Patrimônio (Próprio e Estadual) */}
                    {form.tipo_frota_id && ['1', '4'].includes(String(form.tipo_frota_id)) && (
                      <>
                        <div>
                          <label className="block text-sm font-medium mb-1">Número Patrimônio</label>
                          <input
                            type="text"
                            className="w-full px-3 py-2 border rounded-lg"
                            value={form.numero_patrimonio || ''}
                            onChange={(e) => setForm({ ...form, numero_patrimonio: e.target.value })}
                            placeholder="Ex: PAT-2024-001"
                          />
                        </div>
                        <div>
                          <label className="block text-sm font-medium mb-1">Valor de Aquisição (R$)</label>
                          <input
                            type="number"
                            step="0.01"
                            className="w-full px-3 py-2 border rounded-lg"
                            value={form.valor_aquisicao || ''}
                            onChange={(e) => setForm({ ...form, valor_aquisicao: e.target.value ? parseFloat(e.target.value) : undefined })}
                            placeholder="0.00"
                          />
                        </div>
                        <div className="col-span-2">
                          <label className="block text-sm font-medium mb-1">Tipo de Aquisição</label>
                          <select
                            className="w-full px-3 py-2 border rounded-lg"
                            value={form.tipo_aquisicao || ''}
                            onChange={(e) => setForm({ ...form, tipo_aquisicao: e.target.value as any })}
                          >
                            <option value="">Selecione...</option>
                            <option value="COMPRADO">💳 Comprado</option>
                            <option value="DOADO">🎁 Doado</option>
                          </select>
                        </div>
                      </>
                    )}

                    {/* Campos para Convênio (PM, Bombeiros) */}
                    {form.tipo_frota_id && String(form.tipo_frota_id) === '3' && (
                      <div className="col-span-2">
                        <label className="block text-sm font-medium mb-1">Tipo de Convênio</label>
                        <select
                          className="w-full px-3 py-2 border rounded-lg"
                          value={form.tipo_convenio || ''}
                          onChange={(e) => setForm({ ...form, tipo_convenio: e.target.value as any })}
                        >
                          <option value="">Selecione...</option>
                          <option value="PM">🚔 PM</option>
                          <option value="BOMBEIROS">🚒 Bombeiros</option>
                        </select>
                      </div>
                    )}

                    {/* Campos para Locado */}
                    {form.tipo_frota_id && String(form.tipo_frota_id) === '2' && (
                      <>
                        <div className="col-span-2">
                          <label className="block text-sm font-medium mb-1">Nome da Locadora</label>
                          <input
                            type="text"
                            className="w-full px-3 py-2 border rounded-lg"
                            value={form.nome_locador || ''}
                            onChange={(e) => setForm({ ...form, nome_locador: e.target.value })}
                            placeholder="Ex: Empresa Locadora XYZ"
                          />
                        </div>
                        <div className="col-span-2">
                          <label className="block text-sm font-medium mb-1">Valor Locação (R$/mês)</label>
                          <input
                            type="number"
                            step="0.01"
                            className="w-full px-3 py-2 border rounded-lg"
                            value={form.valor_locacao || ''}
                            onChange={(e) => setForm({ ...form, valor_locacao: e.target.value ? parseFloat(e.target.value) : undefined })}
                            placeholder="0.00"
                          />
                        </div>
                      </>
                    )}

                    {/* Lotação / Administrativo */}
                    <div className="col-span-2 border-t pt-4 mt-2">
                      <h4 className="font-semibold text-sm mb-3">Lotação</h4>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Unidade</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.unidade_id || ''}
                        onChange={(e) => {
                          const id = parseInt(e.target.value)
                          setUnidadeId(id || null)
                          setForm({ ...form, unidade_id: id || undefined, subunidade_id: undefined })
                        }}
                      >
                        <option value="">Selecione...</option>
                        {unidades?.map((u) => (
                          <option key={u.id} value={u.id}>{u.nome}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Subunidade</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.subunidade_id || ''}
                        onChange={(e) => setForm({ ...form, subunidade_id: e.target.value ? parseInt(e.target.value) : undefined })}
                        disabled={!unidadeId}
                      >
                        <option value="">Selecione...</option>
                        {subunidades?.map((s) => (
                          <option key={s.id} value={s.id}>{s.nome}</option>
                        ))}
                      </select>
                    </div>
                    <div className="col-span-2">
                      <label className="block text-sm font-medium mb-1">Centro de Custo</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.centro_custo_id || ''}
                        onChange={(e) => setForm({ ...form, centro_custo_id: e.target.value ? parseInt(e.target.value) : undefined })}
                      >
                        <option value="">Selecione...</option>
                        {centrosCusto?.map((cc) => (
                          <option key={cc.id} value={cc.id}>{cc.codigo} - {cc.nome}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* 🔧 Dados Técnicos */}
              {activeTab === 'tecnico' && (
                <div className="bg-white rounded-lg p-6 space-y-4">
                  <h3 className="font-bold text-lg mb-4">Dados Técnicos</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Motorização</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.motorizacao || ''}
                        onChange={(e) => setForm({ ...form, motorizacao: e.target.value })}
                        placeholder="Ex: 1.0 Turbo"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Cilindrada (cc)</label>
                      <input
                        type="number"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.cilindrada || ''}
                        onChange={(e) => setForm({ ...form, cilindrada: e.target.value ? parseInt(e.target.value) : undefined })}
                        placeholder="Ex: 1600"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Potência (cv)</label>
                      <input
                        type="number"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.potencia || ''}
                        onChange={(e) => setForm({ ...form, potencia: e.target.value ? parseInt(e.target.value) : undefined })}
                        placeholder="Ex: 110"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Transmissão</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.transmissao || ''}
                        onChange={(e) => setForm({ ...form, transmissao: e.target.value })}
                      >
                        <option value="">Selecione...</option>
                        <option value="MANUAL">Manual</option>
                        <option value="AUTOMATICA">Automática</option>
                        <option value="CVT">CVT</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Tração</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.tracao || ''}
                        onChange={(e) => setForm({ ...form, tracao: e.target.value })}
                      >
                        <option value="">Selecione...</option>
                        <option value="2WD">2WD</option>
                        <option value="4WD">4WD</option>
                        <option value="FWD">FWD</option>
                        <option value="RWD">RWD</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Direção</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.direcao || ''}
                        onChange={(e) => setForm({ ...form, direcao: e.target.value })}
                      >
                        <option value="">Selecione...</option>
                        <option value="MANUAL">Manual</option>
                        <option value="HIDRAULICA">Hidráulica</option>
                        <option value="ELETRICA">Elétrica</option>
                      </select>
                    </div>
                    <div className="col-span-2">
                      <div className="flex items-center gap-4">
                        <label className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={form.vidros_eletricos || false}
                            onChange={(e) => setForm({ ...form, vidros_eletricos: e.target.checked })}
                            className="w-4 h-4 cursor-pointer"
                          />
                          <span className="text-sm">Vidros Elétricos</span>
                        </label>
                        <label className="flex items-center gap-2 cursor-pointer">
                          <input
                            type="checkbox"
                            checked={form.ar_condicionado || false}
                            onChange={(e) => setForm({ ...form, ar_condicionado: e.target.checked })}
                            className="w-4 h-4 cursor-pointer"
                          />
                          <span className="text-sm">Ar Condicionado</span>
                        </label>
                      </div>
                    </div>
                    <div className="col-span-2 border-t pt-4">
                      <h4 className="font-semibold text-sm mb-3">Dados do Pneu</h4>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Dimensões (Ex: 195/65R15)</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.pneu_dimensao || ''}
                        onChange={(e) => setForm({ ...form, pneu_dimensao: e.target.value })}
                        placeholder="195/65R15"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Índice de Velocidade</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.pneu_velocidade || ''}
                        onChange={(e) => setForm({ ...form, pneu_velocidade: e.target.value })}
                        placeholder="Ex: H, V, W"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Índice de Carga</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.pneu_carga || ''}
                        onChange={(e) => setForm({ ...form, pneu_carga: e.target.value })}
                        placeholder="Ex: 91, 92, 93"
                      />
                    </div>
                  </div>
                </div>
              )}

              {/* ⚙️ Operacional */}
              {activeTab === 'operacional' && (
                <div className="bg-white rounded-lg p-6 space-y-4">
                  <h3 className="font-bold text-lg mb-4">Dados Operacionais</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Tipo Controle</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.tipo_controle || ''}
                        onChange={(e) => setForm({ ...form, tipo_controle: e.target.value as any })}
                      >
                        <option value="QUILOMETRAGEM">Quilometragem</option>
                        <option value="HORIMETRO">Horimetro</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Leitura Inicial</label>
                      <input
                        type="number"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.hodometro_horimetro_inicial || 0}
                        onChange={(e) => setForm({ ...form, hodometro_horimetro_inicial: parseInt(e.target.value) || 0 })}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Capacidade Tanque (L)</label>
                      <input
                        type="number"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.capacidade_tanque || ''}
                        onChange={(e) => setForm({ ...form, capacidade_tanque: e.target.value ? parseInt(e.target.value) : undefined })}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Capacidade Passageiros</label>
                      <input
                        type="number"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.capacidade_passageiros || ''}
                        onChange={(e) => setForm({ ...form, capacidade_passageiros: e.target.value ? parseInt(e.target.value) : undefined })}
                      />
                    </div>
                    <div className="col-span-2">
                      <label className="block text-sm font-medium mb-1">Capacidade Carga (kg)</label>
                      <input
                        type="number"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.capacidade_carga || ''}
                        onChange={(e) => setForm({ ...form, capacidade_carga: e.target.value ? parseInt(e.target.value) : undefined })}
                      />
                    </div>

                  </div>
                </div>
              )}

              {/* 📄 Documentação */}
              {activeTab === 'documentacao' && (
                <div className="bg-white rounded-lg p-6 space-y-6">
                  <div>
                    <h3 className="font-bold text-lg mb-4">Documentação</h3>
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <label className="block text-sm font-medium mb-1">Vencimento Licenciamento</label>
                        <input
                          type="date"
                          className="w-full px-3 py-2 border rounded-lg"
                          value={form.vencimento_licenciamento ? String(form.vencimento_licenciamento).split('T')[0] : ''}
                          onChange={(e) => setForm({ ...form, vencimento_licenciamento: e.target.value as any })}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-1">Vencimento Seguro</label>
                        <input
                          type="date"
                          className="w-full px-3 py-2 border rounded-lg"
                          value={form.vencimento_seguro ? String(form.vencimento_seguro).split('T')[0] : ''}
                          onChange={(e) => setForm({ ...form, vencimento_seguro: e.target.value as any })}
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium mb-1">Vencimento IPVA</label>
                        <input
                          type="date"
                          className="w-full px-3 py-2 border rounded-lg"
                          value={form.vencimento_ipva ? String(form.vencimento_ipva).split('T')[0] : ''}
                          onChange={(e) => setForm({ ...form, vencimento_ipva: e.target.value as any })}
                        />
                      </div>
                    </div>
                  </div>

                  {/* Seção de Arquivos */}
                  <div className="border-t pt-6">
                    <h4 className="font-bold text-base mb-4">Arquivos Anexados</h4>
                    <div className="space-y-4">
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <label className="block text-sm font-medium mb-1">Tipo de Documento</label>
                          <select className="w-full px-3 py-2 border rounded-lg text-sm">
                            <option value="">Selecione...</option>
                            <option value="FOTO_VEICULO">Foto do Veículo</option>
                            <option value="CRLV">CRLV</option>
                            <option value="NF_COMPRA">NF de Compra</option>
                            <option value="APOL_SEGURO">Apólice de Seguro</option>
                            <option value="MANUTENCAO">Registro de Manutenção</option>
                            <option value="INSPECAO">Inspecção Técnica</option>
                            <option value="OUTRO">Outro</option>
                          </select>
                        </div>
                        <div>
                          <label className="block text-sm font-medium mb-1">Arquivo</label>
                          <input
                            type="file"
                            className="w-full px-3 py-2 border rounded-lg text-sm"
                            accept="image/*,.pdf"
                          />
                        </div>
                      </div>
                      <button
                        type="button"
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700"
                      >
                        ➕ Adicionar Arquivo
                      </button>

                      {/* Lista de Arquivos (vazia por enquanto) */}
                      <div className="mt-4">
                        <p className="text-sm text-gray-500 italic">Nenhum arquivo anexado ainda.</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Footer */}
            <div className="border-t px-6 py-4 flex justify-end gap-3 shrink-0 bg-white">
              <button
                onClick={() => setShowForm(false)}
                className="px-4 py-2 border rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                onClick={handleSave}
                disabled={createMutation.isPending || updateMutation.isPending}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
              >
                {createMutation.isPending || updateMutation.isPending ? 'Salvando...' : 'Salvar'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ── Modal de Detalhes ─────────────────────────────────────────── */}
      {showDetail && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl h-[90vh] flex flex-col overflow-hidden">

            {/* Hero Header */}
            <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-3 text-white shrink-0 relative">
              {!loadingDetail && detailVeiculo && (
                <div className="flex items-center justify-between">
                  <div className="flex items-baseline gap-3">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold border ${
                      isAtivo(detailVeiculo.situacao)
                        ? 'bg-green-500/20 text-green-100 border-green-400/40'
                        : (detailVeiculo.situacao as string) === 'MANUTENCAO'
                          ? 'bg-amber-500/20 text-amber-100 border-amber-400/40'
                          : 'bg-red-500/20 text-red-100 border-red-400/40'
                    }`}>
                      {situacaoBadge(detailVeiculo.situacao).label}
                    </span>
                    <h2 className="text-4xl font-bold font-mono tracking-wide">
                      {detailVeiculo.placa}
                    </h2>
                    <p className="text-blue-100 text-sm">
                      {detailVeiculo.marca?.nome} {detailVeiculo.modelo?.nome} · {detailVeiculo.ano_fabricacao}
                    </p>
                  </div>
                  <button
                    onClick={() => setShowDetail(false)}
                    className="text-white hover:text-gray-200 text-2xl leading-none transition-colors"
                  >
                    ✕
                  </button>
                </div>
              )}

              {loadingDetail && (
                <div className="flex items-center gap-2 text-blue-100">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                  <span className="text-sm">Carregando...</span>
                </div>
              )}
            </div>

            {/* Body: Foto + Info */}
            <div className="flex-1 overflow-y-auto bg-gray-50 no-scrollbar">
              {loadingDetail ? (
                <div className="flex flex-col items-center justify-center h-96 text-gray-400 gap-3">
                  <div className="animate-spin rounded-full h-9 w-9 border-b-2 border-blue-600" />
                  <p className="text-sm">Carregando dados...</p>
                </div>
              ) : detailVeiculo ? (
                <>
                  {/* Grid: Foto + Quick Stats + Tabs + Cards */}
                  <div className="p-6 space-y-4">

                    {/* Foto + Quick Stats + Tabs em uma linha */}
                    <div className="grid grid-cols-3 gap-4">
                      {/* Foto (col-span-1) */}
                      <div className="col-span-1 flex flex-col gap-4">
                        {/* Placeholder de foto */}
                        <div className="bg-white rounded-xl border-2 border-gray-200 h-40 flex items-center justify-center">
                          <div className="text-center">
                            <div className="text-4xl mb-2">🚗</div>
                            <p className="text-xs text-gray-400">Foto</p>
                          </div>
                        </div>

                        {/* Quick Stats abaixo */}
                        <div className="grid grid-cols-2 gap-2">
                          {[
                            { label: 'PREFIXO', value: detailVeiculo.prefixo || '—' },
                            { label: 'COMBUSTÍVEL', value: detailVeiculo.combustivel },
                            { label: 'TIPO', value: (detailVeiculo.tipo_veiculo_nome ?? '—').replace(/_/g, ' ').slice(0, 15) },
                            { label: 'CATEGORIA', value: detailVeiculo.categoria?.nome?.slice(0, 12) || '—' },
                          ].map(({ label, value }) => (
                            <div key={label} className="bg-white rounded-lg p-3 border border-gray-100">
                              <p className="text-gray-500 text-xs font-bold tracking-wide">{label}</p>
                              <p className="text-gray-900 font-bold text-sm mt-1 truncate">{value}</p>
                            </div>
                          ))}
                        </div>
                      </div>

                      {/* Info Panels (col-span-2) */}
                      <div className="col-span-2 space-y-3">
                        {/* Tabs */}
                        <div className="flex gap-2 border-b border-gray-200 overflow-x-auto">
                          {[
                            { id: 'gerais', label: 'Dados Gerais' },
                            { id: 'classificacao', label: 'Frota' },
                            { id: 'tecnico', label: 'Técnico' },
                            { id: 'operacional', label: 'Operação' },
                          ].map((tab) => (
                            <button
                              key={tab.id}
                              onClick={() => setActiveTab(tab.id)}
                              className={`px-4 py-2 text-xs font-medium border-b-2 transition-colors whitespace-nowrap ${
                                activeTab === tab.id
                                  ? 'border-blue-600 text-blue-600'
                                  : 'border-transparent text-gray-600 hover:text-gray-900'
                              }`}
                            >
                              {tab.label}
                            </button>
                          ))}
                        </div>

                        {/* Tab Content */}
                        <div className="bg-white rounded-lg p-4 space-y-2 max-h-80 overflow-y-auto border border-gray-100 no-scrollbar">
                          {activeTab === 'gerais' && (
                            <>
                              <InfoRow label="RENAVAM" value={detailVeiculo.renavam} mono />
                              <InfoRow label="Chassi" value={detailVeiculo.chassi} mono />
                              <InfoRow label="Cor" value={detailVeiculo.cor} />
                              <InfoRow label="Motorização" value={detailVeiculo.motorizacao} />
                              <InfoRow label="UF" value={detailVeiculo.uf} />
                              <InfoRow label="Município" value={detailVeiculo.municipio} />
                            </>
                          )}

                          {activeTab === 'classificacao' && (
                            <>
                              <InfoRow label="Tipo de Frota" value={tiposFrota?.find(t => t.id === detailVeiculo.tipo_frota_id)?.nome} />
                              <InfoRow label="Nº Patrimônio" value={detailVeiculo.numero_patrimonio} />
                              <InfoRow label="Tipo Aquisição" value={detailVeiculo.tipo_aquisicao} />
                              <InfoRow
                                label="Valor Aquisição"
                                value={detailVeiculo.valor_aquisicao != null
                                  ? `R$ ${detailVeiculo.valor_aquisicao.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
                                  : null}
                              />
                              <InfoRow label="Locadora" value={detailVeiculo.nome_locador} />
                              <InfoRow
                                label="Valor Locação"
                                value={detailVeiculo.valor_locacao != null
                                  ? `R$ ${detailVeiculo.valor_locacao.toFixed(2)}/mês`
                                  : null}
                              />
                              <InfoRow label="Unidade" value={detailVeiculo.unidade?.nome} />
                              <InfoRow label="Subunidade" value={detailVeiculo.subunidade?.nome} />
                              <InfoRow
                                label="Centro de Custo"
                                value={detailVeiculo.centro_custo
                                  ? `${detailVeiculo.centro_custo.codigo} — ${detailVeiculo.centro_custo.nome}`
                                  : null}
                              />
                            </>
                          )}

                          {activeTab === 'tecnico' && (
                            <>
                              <InfoRow label="Cilindrada" value={detailVeiculo.cilindrada ? `${detailVeiculo.cilindrada} cc` : null} />
                              <InfoRow label="Potência" value={detailVeiculo.potencia ? `${detailVeiculo.potencia} cv` : null} />
                              <InfoRow label="Transmissão" value={detailVeiculo.transmissao} />
                              <InfoRow label="Tração" value={detailVeiculo.tracao} />
                              <InfoRow label="Direção" value={detailVeiculo.direcao} />
                              <InfoRow label="Vidros Elétricos" value={detailVeiculo.vidros_eletricos != null ? (detailVeiculo.vidros_eletricos ? 'Sim' : 'Não') : null} />
                              <InfoRow label="Ar Condicionado" value={detailVeiculo.ar_condicionado != null ? (detailVeiculo.ar_condicionado ? 'Sim' : 'Não') : null} />
                              {detailVeiculo.pneu_dimensao && (
                                <InfoRow
                                  label="Pneu"
                                  value={[detailVeiculo.pneu_dimensao, detailVeiculo.pneu_velocidade, detailVeiculo.pneu_carga].filter(Boolean).join(' · ')}
                                />
                              )}
                            </>
                          )}

                          {activeTab === 'operacional' && (
                            <>
                              <InfoRow label="Tipo de Controle" value={detailVeiculo.tipo_controle} />
                              <InfoRow label="Leitura Inicial" value={detailVeiculo.hodometro_horimetro_inicial} />
                              <InfoRow label="Cap. Tanque" value={detailVeiculo.capacidade_tanque ? `${detailVeiculo.capacidade_tanque} L` : null} />
                              <InfoRow label="Cap. Passageiros" value={detailVeiculo.capacidade_passageiros} />
                              <InfoRow label="Cap. Carga" value={detailVeiculo.capacidade_carga ? `${detailVeiculo.capacidade_carga} kg` : null} />
                            </>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Observações (full width) */}
                    {detailVeiculo.observacoes && (
                      <div className="bg-white rounded-lg p-4 border border-gray-100">
                        <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wide mb-2">Observações</h4>
                        <p className="text-sm text-gray-600 leading-relaxed">{detailVeiculo.observacoes}</p>
                      </div>
                    )}

                    {/* Documentação (full width) */}
                    <div className="grid grid-cols-3 gap-3">
                      {[
                        { label: 'IPVA', value: fmtDate(detailVeiculo.vencimento_ipva) },
                        { label: 'LICENCIAMENTO', value: fmtDate(detailVeiculo.vencimento_licenciamento) },
                        { label: 'SEGURO', value: fmtDate(detailVeiculo.vencimento_seguro) },
                      ].map(({ label, value }) => (
                        <div key={label} className="bg-white rounded-lg p-4 border border-gray-100">
                          <p className="text-gray-500 text-xs font-bold tracking-wide">{label}</p>
                          <p className="text-gray-900 font-bold text-sm mt-1">{value || '—'}</p>
                        </div>
                      ))}
                    </div>

                  </div>
                </>
              ) : null}
            </div>

            {/* Footer */}
            <div className="border-t px-6 py-4 flex justify-end gap-3 bg-white shrink-0">
              {detailVeiculo && (
                <button
                  onClick={() => { setShowDetail(false); openEdit(detailVeiculo) }}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium transition-colors"
                >
                  <FiEdit2 size={14} />
                  Editar
                </button>
              )}
              <button
                onClick={() => setShowDetail(false)}
                className="px-4 py-2 border border-gray-200 rounded-lg text-gray-700 hover:bg-gray-50 text-sm font-medium transition-colors"
              >
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  )
}
