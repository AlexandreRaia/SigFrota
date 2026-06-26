'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { veiculoService } from '@/services/veiculos'
import type { Veiculo, VeiculoListItem } from '@/types'
import { FiEdit2, FiPower, FiX, FiArrowLeft, FiPlus, FiSearch, FiSave } from 'react-icons/fi'
import { HiOutlineTruck } from 'react-icons/hi'

// ── masks ─────────────────────────────────────────────────────────────────────

const formatPlaca = (value: string): string => {
  const c = value.toUpperCase().replace(/[^A-Z0-9]/g, '')
  if (c.length >= 4) {
    const mm = c.match(/^([A-Z]{2})(\d)([A-Z]{2})(\d{4})/)
    if (mm) return `${mm[1]}${mm[2]}${mm[3]}-${mm[4]}`.slice(0, 9)
    const m = c.match(/^([A-Z]{3})(\d{4})/)
    if (m) return `${m[1]}-${m[2]}`
  }
  return c.slice(0, 8)
}
const formatRenavam = (v: string) => v.replace(/\D/g, '').slice(0, 11)
const formatChassi  = (v: string) => v.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 17)
const fmtDate = (v: string | null | undefined) =>
  v ? new Date(v + 'T12:00:00').toLocaleDateString('pt-BR') : null

// ── scrollbar hide (once) ─────────────────────────────────────────────────────

if (typeof document !== 'undefined' && !document.getElementById('noscroll-style')) {
  const s = document.createElement('style')
  s.id = 'noscroll-style'
  s.textContent = '.noscroll::-webkit-scrollbar{display:none}.noscroll{-ms-overflow-style:none;scrollbar-width:none}'
  document.head.appendChild(s)
}

// ── shared classes ────────────────────────────────────────────────────────────

const inp = [
  'w-full px-3 py-2 text-sm rounded-lg',
  'border border-gray-200 dark:border-gray-600',
  'bg-white dark:bg-gray-700/60',
  'text-gray-900 dark:text-gray-100',
  'placeholder-gray-400 dark:placeholder-gray-500',
  'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent',
  'disabled:opacity-50 disabled:cursor-not-allowed',
  'transition-colors',
].join(' ')

// ── tiny helpers ──────────────────────────────────────────────────────────────

function InfoRow({
  label, value, mono = false,
}: { label: string; value?: string | number | null; mono?: boolean }) {
  const empty = value == null || value === ''
  return (
    <div className="flex justify-between items-baseline gap-3 py-2.5 border-b border-gray-100 dark:border-gray-700/50 last:border-0">
      <span className="text-xs text-gray-500 dark:text-gray-400 font-medium shrink-0 uppercase tracking-wide">
        {label}
      </span>
      <span className={`text-sm text-right truncate max-w-[60%] ${
        mono ? 'font-mono text-xs' : ''
      } ${empty ? 'text-gray-300 dark:text-gray-600' : 'text-gray-800 dark:text-gray-100'}`}>
        {empty ? '—' : String(value)}
      </span>
    </div>
  )
}

function StatusBadge({ situacao }: { situacao: string }) {
  const isAtivo = situacao === 'ATIVO' || situacao === 'ATIVA'
  const isMaint = situacao === 'MANUTENCAO'
  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-semibold ${
      isAtivo
        ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-300'
        : isMaint
          ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'
          : 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
    }`}>
      <span className="text-[8px]">●</span>
      {isAtivo ? 'Ativo' : isMaint ? 'Manutenção' : 'Inativo'}
    </span>
  )
}

function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4 pb-2 border-b border-gray-100 dark:border-gray-700">
      {children}
    </h3>
  )
}

function Lbl({ children, required }: { children: React.ReactNode; required?: boolean }) {
  return (
    <label className="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1.5">
      {children}{required && <span className="text-red-500 ml-0.5">*</span>}
    </label>
  )
}

// ── tab configs ───────────────────────────────────────────────────────────────

const FORM_TABS = [
  { id: 'gerais',         label: 'Dados Gerais' },
  { id: 'classificacao',  label: 'Frota' },
  { id: 'tecnico',        label: 'Técnico' },
  { id: 'administrativa', label: 'Administrativa' },
  { id: 'operacional',    label: 'Operacional' },
  { id: 'documentacao',   label: 'Documentação' },
]

const VIEW_TABS = [
  { id: 'ident',   label: 'Identificação' },
  { id: 'frota',   label: 'Frota' },
  { id: 'tecnico', label: 'Técnico' },
  { id: 'admin',   label: 'Administrativo' },
]

type ModalMode = 'view' | 'edit' | 'create'

function emptyForm(): Partial<Veiculo> {
  return {
    placa: '', prefixo: '', chassi: '', renavam: '',
    ano_fabricacao: new Date().getFullYear(),
    ano_modelo: new Date().getFullYear() + 1,
    combustivel: 'FLEX' as any,
    tipo_registro_id: 1,
    uf: 'SP', situacao: 'ATIVO' as any,
    tipo_controle: 'QUILOMETRAGEM' as any,
    hodometro_horimetro_inicial: 0,
    tipo_convenio: null,
    cor: '', motorizacao: '', observacoes: '',
    vidros_eletricos: false, ar_condicionado: false,
  }
}

// ── main component ────────────────────────────────────────────────────────────

export default function Veiculos() {
  // list
  const [q, setQ]         = useState('')
  const [situacao, setSit] = useState('')

  // modal
  const [modalOpen,    setModalOpen]    = useState(false)
  const [mode,         setMode]         = useState<ModalMode>('view')
  const [modalLoading, setModalLoading] = useState(false)
  const [detailV,      setDetailV]      = useState<Veiculo | null>(null)
  const [activeTab,    setActiveTab]    = useState('gerais')
  const [viewTab,      setViewTab]      = useState('ident')

  // form
  const [form,      setForm]      = useState<Partial<Veiculo>>(emptyForm())
  const [marcaId,   setMarcaId]   = useState<number | null>(null)
  const [unidadeId, setUnidadeId] = useState<number | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const [successMsg,setSuccess]   = useState<string | null>(null)

  // ── queries ────────────────────────────────────────────────────────────────

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

  const { data: modelos } = useQuery({
    queryKey: ['veiculos', 'modelos', marcaId],
    queryFn: () => marcaId ? veiculoService.modelos(marcaId) : Promise.resolve([]),
    enabled: !!marcaId,
  })

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

  const qc = useQueryClient()

  // ── mutations ──────────────────────────────────────────────────────────────

  const createMut = useMutation<Veiculo, Error, Partial<Veiculo>>({
    mutationFn: (d) => veiculoService.criar(d),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['veiculos'] })
      setSuccess('Veículo criado com sucesso!')
      setTimeout(() => { setSuccess(null); setModalOpen(false) }, 1500)
    },
  })

  const updateMut = useMutation<Veiculo, Error, { id: number; data: Partial<Veiculo> }>({
    mutationFn: ({ id, data }) => veiculoService.atualizar(id, data),
    onSuccess: (updated) => {
      qc.invalidateQueries({ queryKey: ['veiculos'] })
      setSuccess('Veículo atualizado!')
      setDetailV(updated)
      setTimeout(() => { setSuccess(null); setMode('view'); setViewTab('ident') }, 1200)
    },
  })

  const toggleMut = useMutation<Veiculo, Error, VeiculoListItem>({
    mutationFn: (v) => {
      const ativo = v.situacao === 'ATIVO' || (v.situacao as string) === 'ATIVA'
      return ativo ? veiculoService.inativar(v.id) : veiculoService.ativar(v.id)
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ['veiculos'] }),
  })

  const isSaving = createMut.isPending || updateMut.isPending

  // ── handlers ──────────────────────────────────────────────────────────────

  function openCreate() {
    setForm(emptyForm())
    setMarcaId(null); setUnidadeId(null)
    setMode('create'); setActiveTab('gerais')
    setFormError(null); setSuccess(null)
    setModalOpen(true)
  }

  async function openView(v: VeiculoListItem) {
    setModalLoading(true)
    setDetailV(null)
    setMode('view'); setViewTab('ident')
    setModalOpen(true)
    try {
      const full = await veiculoService.detalhe(v.id)
      setDetailV(full)
    } finally {
      setModalLoading(false)
    }
  }

  function switchToEdit() {
    if (!detailV) return
    setForm({ ...detailV })
    setMarcaId(detailV.marca?.id ?? null)
    setUnidadeId(detailV.unidade?.id ?? null)
    setActiveTab('gerais')
    setFormError(null); setSuccess(null)
    setMode('edit')
  }

  function switchToView() {
    setMode('view'); setViewTab('ident')
    setFormError(null); setSuccess(null)
  }

  function closeModal() {
    setModalOpen(false)
    setDetailV(null)
    setFormError(null); setSuccess(null)
  }

  async function handleSave() {
    setFormError(null)
    if (!form.placa?.trim())                              return setFormError('Placa é obrigatória')
    if (!form.prefixo?.trim())                            return setFormError('Prefixo é obrigatório')
    if (!form.chassi?.trim() || form.chassi.length !== 17) return setFormError('Chassi deve ter 17 caracteres')
    if (!form.renavam?.trim() || !/^\d{11}$/.test(form.renavam)) return setFormError('RENAVAM deve ter 11 dígitos')
    if (!marcaId)                                         return setFormError('Marca é obrigatória')
    if (!form.modelo_id)                                  return setFormError('Modelo é obrigatório')
    try {
      const payload = { ...form, marca_id: marcaId }
      if (mode === 'edit' && detailV) {
        await updateMut.mutateAsync({ id: detailV.id, data: payload })
      } else {
        await createMut.mutateAsync(payload)
      }
    } catch (err: any) {
      setFormError(err?.response?.data?.detail || err?.message || 'Erro ao salvar')
    }
  }

  // ── render ────────────────────────────────────────────────────────────────

  return (
    <div className="space-y-5">

      {/* ── page header ─────────────────────────────────────────────────── */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <HiOutlineTruck className="text-blue-500 shrink-0" size={22} />
            Veículos
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400 mt-0.5">
            {isLoading ? '...' : `${veiculos?.length ?? 0} registros`}
          </p>
        </div>
        <button
          onClick={openCreate}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 active:bg-blue-800 text-white text-sm font-medium rounded-lg transition-colors shadow-sm"
        >
          <FiPlus size={15} />
          Novo Veículo
        </button>
      </div>

      {/* ── filters ─────────────────────────────────────────────────────── */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-3.5 flex gap-3 shadow-sm">
        <div className="relative flex-1">
          <FiSearch className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 dark:text-gray-500 pointer-events-none" size={14} />
          <input
            type="text"
            placeholder="Buscar por placa, prefixo..."
            className="w-full pl-8 pr-4 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700/60 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>
        <select
          className="px-3 py-2 text-sm rounded-lg border border-gray-200 dark:border-gray-600 bg-gray-50 dark:bg-gray-700/60 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors"
          value={situacao}
          onChange={(e) => setSit(e.target.value)}
        >
          <option value="">Todas as situações</option>
          <option value="ATIVO">Ativo</option>
          <option value="INATIVO">Inativo</option>
          <option value="MANUTENCAO">Manutenção</option>
        </select>
      </div>

      {/* ── table ───────────────────────────────────────────────────────── */}
      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-100 dark:border-gray-700 bg-gray-50/80 dark:bg-gray-900/40">
              {['Placa / Prefixo', 'Marca / Modelo', 'Ano', 'Combustível', 'Situação', ''].map((h, i) => (
                <th
                  key={i}
                  className={`text-left text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider px-5 py-3.5 ${
                    i === 2 ? 'hidden md:table-cell' : i === 3 ? 'hidden lg:table-cell' : i === 5 ? 'w-20' : ''
                  }`}
                >{h}</th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50 dark:divide-gray-700/30">
            {isLoading ? (
              <tr>
                <td colSpan={6} className="text-center py-16">
                  <div className="inline-block animate-spin rounded-full h-6 w-6 border-2 border-gray-200 dark:border-gray-600 border-t-blue-500 mb-2" />
                  <p className="text-sm text-gray-400">Carregando...</p>
                </td>
              </tr>
            ) : !veiculos?.length ? (
              <tr>
                <td colSpan={6} className="text-center py-16">
                  <HiOutlineTruck className="mx-auto text-gray-300 dark:text-gray-600 mb-2" size={40} />
                  <p className="text-sm text-gray-400 dark:text-gray-500">Nenhum veículo encontrado</p>
                </td>
              </tr>
            ) : veiculos.map((v) => (
              <tr
                key={v.id}
                className="hover:bg-blue-50/30 dark:hover:bg-blue-900/10 transition-colors"
              >
                <td className="px-5 py-3.5">
                  <span className="font-mono font-bold text-gray-900 dark:text-white text-sm">{v.placa}</span>
                  {v.prefixo && (
                    <span className="ml-2 text-xs text-gray-400 dark:text-gray-500 font-normal">{v.prefixo}</span>
                  )}
                </td>
                <td className="px-5 py-3.5 text-sm text-gray-700 dark:text-gray-300">
                  <span className="font-medium">{v.marca?.nome}</span>
                  <span className="text-gray-500 dark:text-gray-400"> {v.modelo?.nome}</span>
                </td>
                <td className="px-5 py-3.5 text-sm text-gray-600 dark:text-gray-400 hidden md:table-cell">
                  {v.ano_fabricacao}
                </td>
                <td className="px-5 py-3.5 text-sm text-gray-600 dark:text-gray-400 hidden lg:table-cell">
                  {v.combustivel}
                </td>
                <td className="px-5 py-3.5">
                  <StatusBadge situacao={v.situacao} />
                </td>
                <td className="px-5 py-3.5">
                  <div className="flex items-center gap-0.5 justify-end">
                    <button
                      title="Ver / Editar"
                      onClick={() => openView(v)}
                      className="p-2 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
                    >
                      <FiEdit2 size={14} />
                    </button>
                    <button
                      title={v.situacao === 'ATIVO' || (v.situacao as string) === 'ATIVA' ? 'Inativar' : 'Ativar'}
                      onClick={() => toggleMut.mutate(v)}
                      disabled={toggleMut.isPending}
                      className={`p-2 rounded-lg transition-colors disabled:opacity-40 ${
                        v.situacao === 'ATIVO' || (v.situacao as string) === 'ATIVA'
                          ? 'text-emerald-500 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20'
                          : 'text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 dark:hover:bg-emerald-900/20'
                      }`}
                    >
                      <FiPower size={14} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* ── unified modal ────────────────────────────────────────────────── */}
      {modalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl w-full max-w-4xl h-[90vh] flex flex-col overflow-hidden border border-gray-200 dark:border-gray-700">

            {/* ── modal header ─────────────────────────────────────────── */}
            {mode === 'view' ? (
              /* VIEW header — gradient blue */
              <div className="shrink-0 bg-gradient-to-r from-blue-600 to-blue-700 dark:from-blue-700 dark:to-blue-800 px-6 py-4 flex items-center justify-between">
                {modalLoading ? (
                  <div className="flex items-center gap-2 text-blue-100">
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-blue-300 border-t-white" />
                    <span className="text-sm">Carregando...</span>
                  </div>
                ) : detailV ? (
                  <div>
                    <div className="flex items-center gap-2.5 flex-wrap">
                      <h2 className="text-2xl font-bold font-mono text-white tracking-wide">{detailV.placa}</h2>
                      <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${
                        detailV.situacao === 'ATIVO' || (detailV.situacao as string) === 'ATIVA'
                          ? 'bg-emerald-400/20 text-emerald-100 border-emerald-300/40'
                          : detailV.situacao === 'MANUTENCAO'
                            ? 'bg-amber-400/20 text-amber-100 border-amber-300/40'
                            : 'bg-red-400/20 text-red-100 border-red-300/40'
                      }`}>
                        {detailV.situacao}
                      </span>
                    </div>
                    <p className="text-blue-100 text-sm mt-0.5">
                      {detailV.marca?.nome} {detailV.modelo?.nome} · {detailV.ano_fabricacao}
                      {detailV.prefixo ? ` · ${detailV.prefixo}` : ''}
                    </p>
                  </div>
                ) : <div />}
                <button
                  onClick={closeModal}
                  className="text-white/70 hover:text-white p-1.5 rounded-lg hover:bg-white/10 transition-colors ml-4"
                >
                  <FiX size={20} />
                </button>
              </div>
            ) : (
              /* EDIT / CREATE header — neutral */
              <div className="shrink-0 border-b border-gray-100 dark:border-gray-700 bg-white dark:bg-gray-800 px-6 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {mode === 'edit' && (
                    <button
                      onClick={switchToView}
                      className="flex items-center gap-1.5 text-sm text-gray-500 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                    >
                      <FiArrowLeft size={15} />
                      <span>Detalhes</span>
                    </button>
                  )}
                  {mode === 'edit' && <span className="text-gray-200 dark:text-gray-600">|</span>}
                  <h2 className="text-base font-semibold text-gray-900 dark:text-white">
                    {mode === 'create' ? 'Novo Veículo' : `Editando · ${detailV?.placa ?? ''}`}
                  </h2>
                </div>
                <button
                  onClick={closeModal}
                  className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 p-1.5 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                >
                  <FiX size={20} />
                </button>
              </div>
            )}

            {/* ── modal body ───────────────────────────────────────────── */}
            <div className="flex-1 overflow-y-auto noscroll bg-gray-50 dark:bg-gray-900/50">

              {/* VIEW mode */}
              {mode === 'view' && (
                <div className="p-6 space-y-4">
                  {modalLoading ? (
                    <div className="flex flex-col items-center justify-center h-64 gap-3 text-gray-400 dark:text-gray-500">
                      <div className="animate-spin rounded-full h-10 w-10 border-2 border-gray-200 dark:border-gray-700 border-t-blue-500" />
                      <p className="text-sm">Carregando dados...</p>
                    </div>
                  ) : detailV ? (
                    <>
                      {/* Quick stats */}
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                        {[
                          { label: 'Prefixo',      value: detailV.prefixo || '—' },
                          { label: 'Combustível',   value: detailV.combustivel },
                          { label: 'Categoria',     value: detailV.categoria?.nome || '—' },
                          { label: 'Tipo Controle', value: (detailV.tipo_controle || '').replace('_', ' ') || '—' },
                        ].map(({ label, value }) => (
                          <div key={label} className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-100 dark:border-gray-700 shadow-sm">
                            <p className="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest">{label}</p>
                            <p className="text-gray-900 dark:text-white font-bold text-sm mt-1 truncate">{value}</p>
                          </div>
                        ))}
                      </div>

                      {/* Tabs + content */}
                      <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 shadow-sm overflow-hidden">
                        <div className="flex overflow-x-auto border-b border-gray-100 dark:border-gray-700 px-2">
                          {VIEW_TABS.map((tab) => (
                            <button
                              key={tab.id}
                              onClick={() => setViewTab(tab.id)}
                              className={`px-4 py-3 text-xs font-medium border-b-2 transition-colors whitespace-nowrap ${
                                viewTab === tab.id
                                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                                  : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                              }`}
                            >
                              {tab.label}
                            </button>
                          ))}
                        </div>
                        <div className="p-5">
                          {viewTab === 'ident' && (
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-10">
                              <div>
                                <InfoRow label="RENAVAM"     value={detailV.renavam}    mono />
                                <InfoRow label="Chassi"      value={detailV.chassi}     mono />
                                <InfoRow label="Cor"         value={detailV.cor} />
                                <InfoRow label="Motorização" value={detailV.motorizacao} />
                              </div>
                              <div>
                                <InfoRow label="UF"           value={detailV.uf} />
                                <InfoRow label="Município"    value={detailV.municipio} />
                                <InfoRow label="Ano Modelo"   value={detailV.ano_modelo} />
                                <InfoRow label="Hodômetro Ini."
                                  value={detailV.hodometro_horimetro_inicial != null
                                    ? `${detailV.hodometro_horimetro_inicial.toLocaleString('pt-BR')} km`
                                    : null}
                                />
                              </div>
                            </div>
                          )}
                          {viewTab === 'frota' && (
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-10">
                              <div>
                                <InfoRow label="Tipo de Frota"
                                  value={tiposFrota?.find(t => t.id === detailV.tipo_frota_id)?.nome} />
                                <InfoRow label="Nº Patrimônio"  value={detailV.numero_patrimonio} />
                                <InfoRow label="Tipo Aquisição" value={detailV.tipo_aquisicao} />
                                <InfoRow label="Valor Aquisição"
                                  value={detailV.valor_aquisicao != null
                                    ? `R$ ${detailV.valor_aquisicao.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
                                    : null}
                                />
                              </div>
                              <div>
                                <InfoRow label="Locadora"
                                  value={detailV.nome_locador} />
                                <InfoRow label="Valor Locação"
                                  value={detailV.valor_locacao != null
                                    ? `R$ ${detailV.valor_locacao.toFixed(2)}/mês`
                                    : null}
                                />
                                <InfoRow label="Tipo Convênio" value={detailV.tipo_convenio} />
                              </div>
                            </div>
                          )}
                          {viewTab === 'tecnico' && (
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-10">
                              <div>
                                <InfoRow label="Cilindrada"   value={detailV.cilindrada ? `${detailV.cilindrada} cc` : null} />
                                <InfoRow label="Potência"     value={detailV.potencia   ? `${detailV.potencia} cv`   : null} />
                                <InfoRow label="Transmissão"  value={detailV.transmissao} />
                                <InfoRow label="Tração"       value={detailV.tracao} />
                              </div>
                              <div>
                                <InfoRow label="Direção"           value={detailV.direcao} />
                                <InfoRow label="Vidros Elétricos"  value={detailV.vidros_eletricos  ? 'Sim' : 'Não'} />
                                <InfoRow label="Ar Condicionado"   value={detailV.ar_condicionado   ? 'Sim' : 'Não'} />
                                {detailV.pneu_dimensao && (
                                  <InfoRow label="Pneu"
                                    value={[detailV.pneu_dimensao, detailV.pneu_velocidade, detailV.pneu_carga].filter(Boolean).join(' · ')}
                                  />
                                )}
                              </div>
                            </div>
                          )}
                          {viewTab === 'admin' && (
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-10">
                              <div>
                                <InfoRow label="Unidade"      value={detailV.unidade?.nome} />
                                <InfoRow label="Subunidade"   value={detailV.subunidade?.nome} />
                                <InfoRow label="Centro Custo"
                                  value={detailV.centro_custo
                                    ? `${detailV.centro_custo.codigo} — ${detailV.centro_custo.descricao}`
                                    : null}
                                />
                              </div>
                              <div>
                                <InfoRow label="Cap. Tanque"      value={detailV.capacidade_tanque      ? `${detailV.capacidade_tanque} L`      : null} />
                                <InfoRow label="Cap. Passageiros" value={detailV.capacidade_passageiros} />
                                <InfoRow label="Cap. Carga"       value={detailV.capacidade_carga       ? `${detailV.capacidade_carga} kg`      : null} />
                              </div>
                            </div>
                          )}
                        </div>
                      </div>

                      {/* Doc vencimentos */}
                      <div className="grid grid-cols-3 gap-3">
                        {[
                          { label: 'IPVA',           value: fmtDate(detailV.vencimento_ipva),           icon: '📅' },
                          { label: 'Licenciamento',  value: fmtDate(detailV.vencimento_licenciamento),  icon: '📄' },
                          { label: 'Seguro',         value: fmtDate(detailV.vencimento_seguro),         icon: '🛡️' },
                        ].map(({ label, value, icon }) => (
                          <div key={label} className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-100 dark:border-gray-700 shadow-sm">
                            <p className="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest flex items-center gap-1.5 mb-1">
                              {icon} {label}
                            </p>
                            <p className={`font-bold text-sm ${value ? 'text-gray-900 dark:text-white' : 'text-gray-300 dark:text-gray-600'}`}>
                              {value || '—'}
                            </p>
                          </div>
                        ))}
                      </div>

                      {/* Observações */}
                      {detailV.observacoes && (
                        <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-100 dark:border-gray-700 shadow-sm">
                          <p className="text-[10px] font-bold text-gray-400 dark:text-gray-500 uppercase tracking-widest mb-2">
                            Observações
                          </p>
                          <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                            {detailV.observacoes}
                          </p>
                        </div>
                      )}
                    </>
                  ) : null}
                </div>
              )}

              {/* EDIT / CREATE mode */}
              {(mode === 'edit' || mode === 'create') && (
                <div className="h-full flex flex-col">

                  {/* Alerts */}
                  {(successMsg || formError) && (
                    <div className="px-6 pt-4 shrink-0 space-y-2">
                      {successMsg && (
                        <div className="rounded-lg bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-700 px-4 py-2.5 text-sm text-emerald-700 dark:text-emerald-300 flex items-center gap-2">
                          ✓ {successMsg}
                        </div>
                      )}
                      {formError && (
                        <div className="rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-700 px-4 py-2.5 text-sm text-red-700 dark:text-red-300 flex items-center gap-2">
                          ⚠ {formError}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Form tabs */}
                  <div className="flex overflow-x-auto border-b border-gray-100 dark:border-gray-700 px-4 pt-3 shrink-0">
                    {FORM_TABS.map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-2.5 text-xs font-medium border-b-2 transition-colors whitespace-nowrap ${
                          activeTab === tab.id
                            ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                            : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200'
                        }`}
                      >
                        {tab.label}
                      </button>
                    ))}
                  </div>

                  {/* Form content */}
                  <div className="flex-1 overflow-y-auto noscroll p-6">
                    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-100 dark:border-gray-700 p-5 shadow-sm">

                      {/* DADOS GERAIS */}
                      {activeTab === 'gerais' && (
                        <div className="space-y-4">
                          <SectionTitle>Identificação do Veículo</SectionTitle>

                          {/* Tipo registro */}
                          <div>
                            <Lbl required>Tipo de Registro</Lbl>
                            <div className="flex gap-6 pt-0.5">
                              {[{ v: 1, l: '🚗 Veículo' }, { v: 2, l: '⚙️ Máquina' }].map(({ v, l }) => (
                                <label key={v} className="flex items-center gap-2 cursor-pointer">
                                  <input type="radio" name="tipo_registro" value={v}
                                    checked={form.tipo_registro_id === v}
                                    onChange={() => setForm({ ...form, tipo_registro_id: v })}
                                    className="w-4 h-4 accent-blue-600" />
                                  <span className="text-sm text-gray-700 dark:text-gray-300">{l}</span>
                                </label>
                              ))}
                            </div>
                          </div>

                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <Lbl required>Placa</Lbl>
                              <input className={inp} value={form.placa || ''} placeholder="ABC-1234"
                                onChange={(e) => setForm({ ...form, placa: formatPlaca(e.target.value) })} />
                            </div>
                            <div>
                              <Lbl required>Prefixo</Lbl>
                              <input className={inp} value={form.prefixo || ''} placeholder="VTR-001"
                                onChange={(e) => setForm({ ...form, prefixo: e.target.value })} />
                            </div>
                            <div>
                              <Lbl required>Chassi (17 caracteres)</Lbl>
                              <input className={inp} value={form.chassi || ''} placeholder="9BWZZZ377VT004251" maxLength={17}
                                onChange={(e) => setForm({ ...form, chassi: formatChassi(e.target.value) })} />
                            </div>
                            <div>
                              <Lbl required>RENAVAM (11 dígitos)</Lbl>
                              <input className={inp} value={form.renavam || ''} placeholder="01234567890" maxLength={11}
                                onChange={(e) => setForm({ ...form, renavam: formatRenavam(e.target.value) })} />
                            </div>
                            <div>
                              <Lbl required>Marca</Lbl>
                              <select className={inp} value={marcaId || ''} onChange={(e) => {
                                const id = parseInt(e.target.value)
                                setMarcaId(id || null)
                                setForm({ ...form, marca_id: id, modelo_id: undefined })
                              }}>
                                <option value="">Selecione...</option>
                                {marcas?.map((m) => <option key={m.id} value={m.id}>{m.nome}</option>)}
                              </select>
                            </div>
                            <div>
                              <Lbl required>Modelo</Lbl>
                              <select className={inp} value={form.modelo_id || ''} disabled={!marcaId}
                                onChange={(e) => setForm({ ...form, modelo_id: parseInt(e.target.value) || undefined })}>
                                <option value="">Selecione...</option>
                                {modelos?.map((m) => <option key={m.id} value={m.id}>{m.nome}</option>)}
                              </select>
                            </div>
                            <div>
                              <Lbl>Ano Fabricação</Lbl>
                              <input type="number" className={inp} value={form.ano_fabricacao || ''} min={1900} max={2030}
                                onChange={(e) => setForm({ ...form, ano_fabricacao: parseInt(e.target.value) })} />
                            </div>
                            <div>
                              <Lbl>Ano Modelo</Lbl>
                              <input type="number" className={inp} value={form.ano_modelo || ''} min={1900} max={2031}
                                onChange={(e) => setForm({ ...form, ano_modelo: parseInt(e.target.value) })} />
                            </div>
                            <div>
                              <Lbl>Cor</Lbl>
                              <input className={inp} value={form.cor || ''} placeholder="Branco"
                                onChange={(e) => setForm({ ...form, cor: e.target.value })} />
                            </div>
                            <div>
                              <Lbl>Combustível</Lbl>
                              <select className={inp} value={form.combustivel || 'FLEX'}
                                onChange={(e) => setForm({ ...form, combustivel: e.target.value as any })}>
                                {['GASOLINA','DIESEL','FLEX','ELETRICO','GNV'].map(c => (
                                  <option key={c} value={c}>{c}</option>
                                ))}
                              </select>
                            </div>
                            <div>
                              <Lbl>Motorização</Lbl>
                              <input className={inp} value={form.motorizacao || ''} placeholder="1.0 MPI"
                                onChange={(e) => setForm({ ...form, motorizacao: e.target.value })} />
                            </div>
                            <div>
                              <Lbl>Situação</Lbl>
                              <select className={inp} value={form.situacao || 'ATIVO'}
                                onChange={(e) => setForm({ ...form, situacao: e.target.value as any })}>
                                <option value="ATIVO">Ativo</option>
                                <option value="INATIVO">Inativo</option>
                                <option value="MANUTENCAO">Manutenção</option>
                              </select>
                            </div>
                            <div>
                              <Lbl>UF</Lbl>
                              <input className={inp} value={form.uf || 'SP'} maxLength={2}
                                onChange={(e) => setForm({ ...form, uf: e.target.value.toUpperCase() })} />
                            </div>
                            <div>
                              <Lbl>Município</Lbl>
                              <input className={inp} value={form.municipio || ''}
                                onChange={(e) => setForm({ ...form, municipio: e.target.value })} />
                            </div>
                            <div className="col-span-2">
                              <Lbl>Observações</Lbl>
                              <textarea className={inp} rows={3} value={form.observacoes || ''}
                                onChange={(e) => setForm({ ...form, observacoes: e.target.value })} />
                            </div>
                          </div>
                        </div>
                      )}

                      {/* FROTA / CLASSIFICAÇÃO */}
                      {activeTab === 'classificacao' && (
                        <div className="space-y-4">
                          <SectionTitle>Classificação da Frota</SectionTitle>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <Lbl>Tipo de Frota</Lbl>
                              <select className={inp} value={form.tipo_frota_id || ''}
                                onChange={(e) => setForm({ ...form, tipo_frota_id: parseInt(e.target.value) || undefined as any })}>
                                <option value="">Selecione...</option>
                                {tiposFrota?.map(t => <option key={t.id} value={t.id}>{t.nome}</option>)}
                              </select>
                            </div>
                            <div>
                              <Lbl>Tipo Aquisição</Lbl>
                              <select className={inp} value={form.tipo_aquisicao || ''}
                                onChange={(e) => setForm({ ...form, tipo_aquisicao: e.target.value || null as any })}>
                                <option value="">—</option>
                                <option value="COMPRADO">Comprado</option>
                                <option value="DOADO">Doado</option>
                              </select>
                            </div>
                            <div>
                              <Lbl>Nº Patrimônio</Lbl>
                              <input className={inp} value={form.numero_patrimonio || ''}
                                onChange={(e) => setForm({ ...form, numero_patrimonio: e.target.value })} />
                            </div>
                            <div>
                              <Lbl>Valor Aquisição (R$)</Lbl>
                              <input type="number" className={inp} value={form.valor_aquisicao ?? ''}
                                onChange={(e) => setForm({ ...form, valor_aquisicao: e.target.value ? parseFloat(e.target.value) : undefined })} />
                            </div>
                            <div>
                              <Lbl>Tipo Convênio</Lbl>
                              <select className={inp} value={form.tipo_convenio || ''}
                                onChange={(e) => setForm({ ...form, tipo_convenio: e.target.value || null as any })}>
                                <option value="">—</option>
                                <option value="PM">PM</option>
                                <option value="BOMBEIROS">Bombeiros</option>
                              </select>
                            </div>
                            <div>
                              <Lbl>Nome Locador</Lbl>
                              <input className={inp} value={form.nome_locador || ''}
                                onChange={(e) => setForm({ ...form, nome_locador: e.target.value })} />
                            </div>
                            <div>
                              <Lbl>Valor Locação (R$/mês)</Lbl>
                              <input type="number" className={inp} value={form.valor_locacao ?? ''}
                                onChange={(e) => setForm({ ...form, valor_locacao: e.target.value ? parseFloat(e.target.value) : undefined })} />
                            </div>
                          </div>
                        </div>
                      )}

                      {/* DADOS TÉCNICOS */}
                      {activeTab === 'tecnico' && (
                        <div className="space-y-4">
                          <SectionTitle>Dados Técnicos</SectionTitle>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <Lbl>Cilindrada (cc)</Lbl>
                              <input type="number" className={inp} value={form.cilindrada ?? ''}
                                onChange={(e) => setForm({ ...form, cilindrada: e.target.value ? parseInt(e.target.value) : undefined })} />
                            </div>
                            <div>
                              <Lbl>Potência (cv)</Lbl>
                              <input type="number" className={inp} value={form.potencia ?? ''}
                                onChange={(e) => setForm({ ...form, potencia: e.target.value ? parseInt(e.target.value) : undefined })} />
                            </div>
                            <div>
                              <Lbl>Transmissão</Lbl>
                              <select className={inp} value={form.transmissao || ''}
                                onChange={(e) => setForm({ ...form, transmissao: e.target.value || null as any })}>
                                <option value="">—</option>
                                <option value="MANUAL">Manual</option>
                                <option value="AUTOMATICA">Automática</option>
                                <option value="CVT">CVT</option>
                              </select>
                            </div>
                            <div>
                              <Lbl>Tração</Lbl>
                              <select className={inp} value={form.tracao || ''}
                                onChange={(e) => setForm({ ...form, tracao: e.target.value || null as any })}>
                                <option value="">—</option>
                                <option value="2WD">2WD</option>
                                <option value="4WD">4WD</option>
                                <option value="FWD">FWD</option>
                                <option value="RWD">RWD</option>
                              </select>
                            </div>
                            <div>
                              <Lbl>Direção</Lbl>
                              <select className={inp} value={form.direcao || ''}
                                onChange={(e) => setForm({ ...form, direcao: e.target.value || null as any })}>
                                <option value="">—</option>
                                <option value="MANUAL">Manual</option>
                                <option value="HIDRAULICA">Hidráulica</option>
                                <option value="ELETRICA">Elétrica</option>
                              </select>
                            </div>
                            <div>
                              <Lbl>Dimensão do Pneu</Lbl>
                              <input className={inp} value={form.pneu_dimensao || ''} placeholder="195/65R15"
                                onChange={(e) => setForm({ ...form, pneu_dimensao: e.target.value })} />
                            </div>
                            <div className="flex items-center gap-6 col-span-2 pt-1">
                              <label className="flex items-center gap-2 cursor-pointer select-none">
                                <input type="checkbox" checked={!!form.vidros_eletricos}
                                  onChange={(e) => setForm({ ...form, vidros_eletricos: e.target.checked })}
                                  className="w-4 h-4 accent-blue-600 rounded" />
                                <span className="text-sm text-gray-700 dark:text-gray-300">Vidros Elétricos</span>
                              </label>
                              <label className="flex items-center gap-2 cursor-pointer select-none">
                                <input type="checkbox" checked={!!form.ar_condicionado}
                                  onChange={(e) => setForm({ ...form, ar_condicionado: e.target.checked })}
                                  className="w-4 h-4 accent-blue-600 rounded" />
                                <span className="text-sm text-gray-700 dark:text-gray-300">Ar Condicionado</span>
                              </label>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* ADMINISTRATIVA */}
                      {activeTab === 'administrativa' && (
                        <div className="space-y-4">
                          <SectionTitle>Vinculação Administrativa</SectionTitle>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <Lbl>Unidade</Lbl>
                              <select className={inp} value={unidadeId || ''}
                                onChange={(e) => {
                                  const id = parseInt(e.target.value)
                                  setUnidadeId(id || null)
                                  setForm({ ...form, unidade_id: id || undefined })
                                }}>
                                <option value="">Selecione...</option>
                                {unidades?.map(u => <option key={u.id} value={u.id}>{u.nome}</option>)}
                              </select>
                            </div>
                            <div>
                              <Lbl>Subunidade</Lbl>
                              <select className={inp} value={form.subunidade_id || ''} disabled={!unidadeId}
                                onChange={(e) => setForm({ ...form, subunidade_id: parseInt(e.target.value) || undefined })}>
                                <option value="">Selecione...</option>
                                {subunidades?.map(s => <option key={s.id} value={s.id}>{s.nome}</option>)}
                              </select>
                            </div>
                            <div className="col-span-2">
                              <Lbl>Centro de Custo</Lbl>
                              <select className={inp} value={form.centro_custo_id || ''}
                                onChange={(e) => setForm({ ...form, centro_custo_id: parseInt(e.target.value) || undefined })}>
                                <option value="">Selecione...</option>
                                {centrosCusto?.map(c => (
                                  <option key={c.id} value={c.id}>{c.codigo} — {c.descricao}</option>
                                ))}
                              </select>
                            </div>
                          </div>
                        </div>
                      )}

                      {/* OPERACIONAL */}
                      {activeTab === 'operacional' && (
                        <div className="space-y-4">
                          <SectionTitle>Dados Operacionais</SectionTitle>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <Lbl>Tipo de Controle</Lbl>
                              <select className={inp} value={form.tipo_controle || 'QUILOMETRAGEM'}
                                onChange={(e) => setForm({ ...form, tipo_controle: e.target.value as any })}>
                                <option value="QUILOMETRAGEM">Quilometragem</option>
                                <option value="HORIMETRO">Horímetro</option>
                              </select>
                            </div>
                            <div>
                              <Lbl>Hodômetro / Horímetro Inicial</Lbl>
                              <input type="number" className={inp} value={form.hodometro_horimetro_inicial ?? 0}
                                onChange={(e) => setForm({ ...form, hodometro_horimetro_inicial: parseInt(e.target.value) || 0 })} />
                            </div>
                            <div>
                              <Lbl>Cap. Tanque (L)</Lbl>
                              <input type="number" className={inp} value={form.capacidade_tanque ?? ''}
                                onChange={(e) => setForm({ ...form, capacidade_tanque: e.target.value ? parseInt(e.target.value) : undefined })} />
                            </div>
                            <div>
                              <Lbl>Cap. Passageiros</Lbl>
                              <input type="number" className={inp} value={form.capacidade_passageiros ?? ''}
                                onChange={(e) => setForm({ ...form, capacidade_passageiros: e.target.value ? parseInt(e.target.value) : undefined })} />
                            </div>
                            <div className="col-span-2">
                              <Lbl>Cap. Carga (kg)</Lbl>
                              <input type="number" className={inp} value={form.capacidade_carga ?? ''}
                                onChange={(e) => setForm({ ...form, capacidade_carga: e.target.value ? parseInt(e.target.value) : undefined })} />
                            </div>
                          </div>
                        </div>
                      )}

                      {/* DOCUMENTAÇÃO */}
                      {activeTab === 'documentacao' && (
                        <div className="space-y-4">
                          <SectionTitle>Vencimentos de Documentos</SectionTitle>
                          <div className="grid grid-cols-2 gap-4">
                            <div>
                              <Lbl>Vencimento IPVA</Lbl>
                              <input type="date" className={inp}
                                value={form.vencimento_ipva ? String(form.vencimento_ipva).split('T')[0] : ''}
                                onChange={(e) => setForm({ ...form, vencimento_ipva: e.target.value as any })} />
                            </div>
                            <div>
                              <Lbl>Vencimento Licenciamento</Lbl>
                              <input type="date" className={inp}
                                value={form.vencimento_licenciamento ? String(form.vencimento_licenciamento).split('T')[0] : ''}
                                onChange={(e) => setForm({ ...form, vencimento_licenciamento: e.target.value as any })} />
                            </div>
                            <div>
                              <Lbl>Vencimento Seguro</Lbl>
                              <input type="date" className={inp}
                                value={form.vencimento_seguro ? String(form.vencimento_seguro).split('T')[0] : ''}
                                onChange={(e) => setForm({ ...form, vencimento_seguro: e.target.value as any })} />
                            </div>
                          </div>
                        </div>
                      )}

                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* ── modal footer ─────────────────────────────────────────── */}
            <div className="shrink-0 border-t border-gray-100 dark:border-gray-700 px-6 py-4 flex items-center justify-between bg-white dark:bg-gray-800">
              {/* left action */}
              <div>
                {mode === 'view' && !modalLoading && detailV && (
                  <button
                    onClick={switchToEdit}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-lg transition-colors shadow-sm"
                  >
                    <FiEdit2 size={14} />
                    Editar Veículo
                  </button>
                )}
              </div>

              {/* right actions */}
              <div className="flex items-center gap-2">
                {(mode === 'edit' || mode === 'create') && (
                  <>
                    <button
                      onClick={mode === 'edit' ? switchToView : closeModal}
                      className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    >
                      {mode === 'edit' ? '← Cancelar edição' : 'Cancelar'}
                    </button>
                    <button
                      onClick={handleSave}
                      disabled={isSaving}
                      className="flex items-center gap-2 px-5 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50 shadow-sm"
                    >
                      {isSaving
                        ? <div className="animate-spin rounded-full h-3.5 w-3.5 border-2 border-blue-200 border-t-white" />
                        : <FiSave size={14} />}
                      {isSaving ? 'Salvando...' : 'Salvar'}
                    </button>
                  </>
                )}
                {mode === 'view' && (
                  <button
                    onClick={closeModal}
                    className="px-4 py-2 text-sm text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                  >
                    Fechar
                  </button>
                )}
              </div>
            </div>

          </div>
        </div>
      )}

    </div>
  )
}
