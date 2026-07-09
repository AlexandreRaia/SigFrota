import { useState, useRef } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { FiFileText, FiEdit2, FiPower } from 'react-icons/fi'

import { condutorService } from '@/services/condutores'
import { Button } from '@/components/ui/Button'
import type { Condutor, CondutorListItem, CondutorDocumento } from '@/types'

// ── Helpers ────────────────────────────────────────────────────────────────────

const TIPO_DOC_ICONE: Record<string, string> = {
  FOTO: '📷', CNH: '🪦', OUTRO: '📎',
}
const TIPO_DOC_LABEL: Record<string, string> = {
  FOTO: 'Foto', CNH: 'CNH Digitalizada', OUTRO: 'Outro',
}
const CNH_CATEGORIAS = ['A', 'B', 'C', 'D', 'E', 'AB', 'AC', 'AD', 'AE', 'ACC']

function isAtivo(status: string) { return status === 'ATIVO' }

function statusBadge(status: string) {
  if (status === 'ATIVO')    return { label: 'Ativo',    cls: 'bg-green-100 text-green-700 border border-green-200' }
  if (status === 'SUSPENSO') return { label: 'Suspenso', cls: 'bg-amber-100 text-amber-700 border border-amber-200' }
  return                            { label: 'Inativo',  cls: 'bg-red-100 text-red-700 border border-red-200' }
}

function cnhVencimentoBadge(vencimento: string | null) {
  if (!vencimento) return null
  const dias = Math.ceil((new Date(vencimento).getTime() - Date.now()) / 86400000)
  if (dias < 0)   return { label: 'CNH Vencida',      cls: 'bg-red-100 text-red-700 border border-red-200' }
  if (dias <= 30) return { label: `Vence em ${dias}d`, cls: 'bg-amber-100 text-amber-700 border border-amber-200' }
  return null
}

function fmtDate(d: string | null | undefined) {
  if (!d) return '—'
  return new Date(d + 'T12:00:00').toLocaleDateString('pt-BR')
}

function InfoRow({ label, value, mono }: { label: string; value: string | number | null | undefined; mono?: boolean }) {
  if (!value && value !== 0) return null
  return (
    <div className="flex items-baseline justify-between gap-4 py-1.5 border-b border-gray-50 last:border-0">
      <span className="text-xs font-normal text-slate-500 shrink-0">{label}</span>
      <span className={`text-sm font-medium text-slate-800 text-right truncate ${mono ? 'font-mono' : ''}`}>{value}</span>
    </div>
  )
}

// ── Component ──────────────────────────────────────────────────────────────────

export default function Condutores() {
  const queryClient = useQueryClient()

  const [q, setQ] = useState('')
  const [statusFiltro, setStatusFiltro] = useState('')

  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState<Condutor | null>(null)
  const [activeFormTab, setActiveFormTab] = useState('identificacao')
  const [form, setForm] = useState<Partial<Condutor>>({})
  const [formError, setFormError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  const [showDetail, setShowDetail] = useState(false)
  const [detailCondutor, setDetailCondutor] = useState<Condutor | null>(null)
  const [loadingDetail, setLoadingDetail] = useState(false)
  const [activeDetailTab, setActiveDetailTab] = useState('pessoal')
  const [carouselIdx, setCarouselIdx] = useState(0)

  const [uploadFile, setUploadFile] = useState<File | null>(null)
  const [uploadTipo, setUploadTipo] = useState('')
  const [uploadDescricao, setUploadDescricao] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)

  // ── Queries ────────────────────────────────────────────────────────────────

  const { data: condutores = [], isLoading } = useQuery<CondutorListItem[]>({
    queryKey: ['condutores', { q, statusFiltro }],
    queryFn: () => condutorService.listar({ q, status: statusFiltro }),
  })

  const { data: unidades = [] } = useQuery({
    queryKey: ['condutores', 'unidades'],
    queryFn: () => condutorService.unidades(),
  })

  const { data: subunidades = [] } = useQuery({
    queryKey: ['condutores', 'subunidades', (form as any).unidade_id],
    queryFn: () => condutorService.subunidades((form as any).unidade_id),
    enabled: !!(form as any).unidade_id,
  })

  const { data: documentos = [], isLoading: loadingDocs } = useQuery<CondutorDocumento[]>({
    queryKey: ['condutor-documentos', editing?.id],
    queryFn: () => condutorService.listarDocumentos(editing!.id),
    enabled: !!editing?.id,
  })

  const { data: detalheDocumentos = [] } = useQuery<CondutorDocumento[]>({
    queryKey: ['condutor-documentos', detailCondutor?.id],
    queryFn: () => condutorService.listarDocumentos(detailCondutor!.id),
    enabled: !!detailCondutor?.id,
  })

  // ── Mutations ──────────────────────────────────────────────────────────────

  const createMutation = useMutation<Condutor, Error, Partial<Condutor>>({
    mutationFn: (data) => condutorService.criar(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['condutores'] })
      setSuccessMessage('Condutor criado com sucesso!')
      setTimeout(() => setShowForm(false), 1000)
    },
  })

  const updateMutation = useMutation<Condutor, Error, { id: number; data: Partial<Condutor> }>({
    mutationFn: ({ id, data }) => condutorService.atualizar(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['condutores'] })
      setSuccessMessage('Condutor atualizado com sucesso!')
      setTimeout(() => setShowForm(false), 1000)
    },
  })

  const toggleStatusMutation = useMutation<Condutor, Error, CondutorListItem>({
    mutationFn: (c) => isAtivo(c.status) ? condutorService.inativar(c.id) : condutorService.ativar(c.id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['condutores'] }),
  })

  const uploadDocMutation = useMutation({
    mutationFn: ({ tipo, descricao, file }: { tipo: string; descricao: string; file: File }) =>
      condutorService.uploadDocumento(editing!.id, tipo, descricao, file),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['condutor-documentos', editing?.id] })
      setUploadFile(null); setUploadTipo(''); setUploadDescricao('')
      if (fileInputRef.current) fileInputRef.current.value = ''
    },
    onError: (err: Error) => setFormError(err.message),
  })

  const deleteDocMutation = useMutation({
    mutationFn: (docId: number) => condutorService.deletarDocumento(editing!.id, docId),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['condutor-documentos', editing?.id] }),
  })

  // ── Handlers ───────────────────────────────────────────────────────────────

  function openCreate() {
    setEditing(null)
    setForm({ status: 'ATIVO', cnh_categoria: 'B' })
    setActiveFormTab('identificacao')
    setFormError(null); setSuccessMessage(null)
    setUploadFile(null); setUploadTipo(''); setUploadDescricao('')
    setShowForm(true)
  }

  async function openEdit(c: CondutorListItem) {
    const full = await condutorService.detalhe(c.id)
    setEditing(full); setForm(full)
    setActiveFormTab('identificacao')
    setFormError(null); setSuccessMessage(null)
    setUploadFile(null); setUploadTipo(''); setUploadDescricao('')
    setShowForm(true)
  }

  async function handleView(c: CondutorListItem) {
    setLoadingDetail(true)
    setDetailCondutor(null)
    setActiveDetailTab('pessoal')
    setCarouselIdx(0)
    setShowDetail(true)
    try {
      const full = await condutorService.detalhe(c.id)
      setDetailCondutor(full)
    } finally {
      setLoadingDetail(false)
    }
  }

  async function handleSave() {
    setFormError(null)
    if (!form.nome?.trim())       { setFormError('Nome é obrigatório'); return }
    if (!form.cpf?.trim())        { setFormError('CPF é obrigatório'); return }
    if (!form.prontuario?.trim()) { setFormError('Prontuário é obrigatório'); return }
    if (!form.data_nascimento)    { setFormError('Data de nascimento é obrigatória'); return }
    if (!form.cnh_numero?.trim()) { setFormError('Número da CNH é obrigatório'); return }
    if (!form.cnh_vencimento)     { setFormError('Vencimento da CNH é obrigatório'); return }
    try {
      if (editing) {
        await updateMutation.mutateAsync({ id: editing.id, data: form })
      } else {
        await createMutation.mutateAsync(form)
      }
    } catch (err: unknown) {
      const e = err as { response?: { data?: { detail?: string } }; message?: string }
      setFormError(e?.response?.data?.detail || e?.message || 'Erro ao salvar')
    }
  }

  function setF(field: string, value: unknown) {
    setForm(prev => ({ ...prev, [field]: value }))
  }

  const isSaving = createMutation.isPending || updateMutation.isPending

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <div className="space-y-4 p-6">

      {/* Cabeçalho */}
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-bold text-slate-800">Condutores</h1>
        <Button onClick={openCreate} className="bg-blue-600 hover:bg-blue-700">
          + Novo Condutor
        </Button>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow p-4 flex gap-4">
        <input type="text" placeholder="🔍 Buscar por nome, CPF, prontuário..."
          className="px-4 py-2 border rounded-lg flex-1" value={q} onChange={(e) => setQ(e.target.value)} />
        <select className="px-4 py-2 border rounded-lg" value={statusFiltro} onChange={(e) => setStatusFiltro(e.target.value)}>
          <option value="">Todos os status</option>
          <option value="ATIVO">Ativo</option>
          <option value="INATIVO">Inativo</option>
          <option value="SUSPENSO">Suspenso</option>
        </select>
      </div>

      {/* Tabela */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Prontuário</th>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Nome</th>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Unidade</th>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Subunidade</th>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Status</th>
              <th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-500">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {isLoading ? (
              <tr><td colSpan={6} className="px-6 py-10 text-center text-slate-400">Carregando...</td></tr>
            ) : condutores.length === 0 ? (
              <tr><td colSpan={6} className="px-6 py-10 text-center text-slate-400">Nenhum condutor encontrado</td></tr>
            ) : condutores.map((c) => {
              const badge = statusBadge(c.status)
              return (
                <tr key={c.id} className="hover:bg-gray-50">
                  <td className="px-6 py-3 font-mono text-sm font-medium text-slate-800">{c.prontuario}</td>
                  <td className="px-6 py-3 text-sm font-medium text-slate-800">{c.nome}</td>
                  <td className="px-6 py-3 text-sm text-slate-600">{c.unidade ? (c.unidade.sigla ? `${c.unidade.sigla} — ${c.unidade.nome}` : c.unidade.nome) : '—'}</td>
                  <td className="px-6 py-3 text-sm text-slate-600">{c.subunidade ? (c.subunidade.sigla ? `${c.subunidade.sigla} — ${c.subunidade.nome}` : c.subunidade.nome) : '—'}</td>
                  <td className="px-6 py-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${badge.cls}`}>{badge.label}</span>
                  </td>
                  <td className="px-6 py-3">
                    <div className="flex items-center gap-0.5">
                      <button title="Ver ficha" onClick={() => handleView(c)}
                        className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                        <FiFileText size={16} />
                      </button>
                      <button title="Editar" onClick={() => openEdit(c)}
                        className="p-2 text-gray-400 hover:text-amber-600 hover:bg-amber-50 rounded-lg transition-colors">
                        <FiEdit2 size={16} />
                      </button>
                      <button
                        title={isAtivo(c.status) ? 'Inativar' : 'Ativar'}
                        onClick={() => toggleStatusMutation.mutate(c)}
                        className={`p-2 rounded-lg transition-colors ${isAtivo(c.status)
                          ? 'text-gray-400 hover:text-red-600 hover:bg-red-50'
                          : 'text-gray-400 hover:text-green-600 hover:bg-green-50'}`}>
                        <FiPower size={16} />
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {/* ── Modal de Formulário ──────────────────────────────────────────── */}
      {showForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-3xl h-[90vh] flex flex-col overflow-hidden">

            <div className="flex items-center justify-between px-6 py-4 border-b shrink-0">
              <h2 className="text-base font-semibold text-slate-800">
                {editing ? '✏️ Editar Condutor' : '➕ Novo Condutor'}
              </h2>
              <button onClick={() => setShowForm(false)} className="text-gray-500 hover:text-gray-700 text-2xl leading-none">✕</button>
            </div>

            <div className="flex gap-0 border-b shrink-0 px-6">
              {[
                { id: 'identificacao', label: 'Identificação' },
                { id: 'pessoal',       label: 'Dados Pessoais' },
                { id: 'cnh',           label: 'CNH' },
                { id: 'contato',       label: 'Contato' },
                { id: 'lotacao',       label: 'Lotação' },
                { id: 'documentos',    label: 'Documentos' },
              ].map(tab => (
                <button key={tab.id} onClick={() => setActiveFormTab(tab.id)}
                  className={`px-3 py-2.5 text-xs font-semibold border-b-2 transition-colors whitespace-nowrap -mb-px ${
                    activeFormTab === tab.id ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-800'
                  }`}>
                  {tab.label}
                </button>
              ))}
            </div>

            <div className="flex-1 overflow-y-auto p-6">

              {activeFormTab === 'identificacao' && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-700">Identificação</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">Prontuário *</label>
                      <input className="input w-full" value={form.prontuario ?? ''} onChange={e => setF('prontuario', e.target.value)} placeholder="Ex: 001234" />
                    </div>
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">Status *</label>
                      <select className="input w-full" value={form.status ?? 'ATIVO'} onChange={e => setF('status', e.target.value)}>
                        <option value="ATIVO">Ativo</option>
                        <option value="INATIVO">Inativo</option>
                        <option value="SUSPENSO">Suspenso</option>
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {activeFormTab === 'pessoal' && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-700">Informações Pessoais</h3>
                  <div>
                    <label className="block text-xs font-normal text-slate-500 mb-1">Nome Completo *</label>
                    <input className="input w-full" value={form.nome ?? ''} onChange={e => setF('nome', e.target.value)} />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">CPF *</label>
                      <input className="input w-full font-mono" value={form.cpf ?? ''} onChange={e => setF('cpf', e.target.value)} placeholder="000.000.000-00" />
                    </div>
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">Data de Nascimento *</label>
                      <input type="date" className="input w-full" value={form.data_nascimento ?? ''} onChange={e => setF('data_nascimento', e.target.value)} />
                    </div>
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">RG</label>
                      <input className="input w-full font-mono" value={form.rg ?? ''} onChange={e => setF('rg', e.target.value)} />
                    </div>
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">Órgão Emissor</label>
                      <input className="input w-full" value={form.orgao_emissor ?? ''} onChange={e => setF('orgao_emissor', e.target.value)} placeholder="Ex: SSP-SP" />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-normal text-slate-500 mb-1">Cargo</label>
                    <input className="input w-full" value={form.cargo ?? ''} onChange={e => setF('cargo', e.target.value)} placeholder="Cargo na Prefeitura" />
                  </div>
                </div>
              )}

              {activeFormTab === 'cnh' && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-700">Habilitação (CNH)</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">Número da CNH *</label>
                      <input className="input w-full font-mono" value={form.cnh_numero ?? ''} onChange={e => setF('cnh_numero', e.target.value)} placeholder="11 dígitos" maxLength={11} />
                    </div>
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">Categoria *</label>
                      <select className="input w-full" value={form.cnh_categoria ?? ''} onChange={e => setF('cnh_categoria', e.target.value)}>
                        <option value="">Selecione...</option>
                        {CNH_CATEGORIAS.map(c => <option key={c} value={c}>{c}</option>)}
                      </select>
                    </div>
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">Data de Emissão</label>
                      <input type="date" className="input w-full" value={form.cnh_emissao ?? ''} onChange={e => setF('cnh_emissao', e.target.value)} />
                    </div>
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">Data de Vencimento *</label>
                      <input type="date" className="input w-full" value={form.cnh_vencimento ?? ''} onChange={e => setF('cnh_vencimento', e.target.value)} />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-normal text-slate-500 mb-1">Órgão Expedidor</label>
                    <input className="input w-full" value={form.cnh_orgao ?? ''} onChange={e => setF('cnh_orgao', e.target.value)} placeholder="Ex: DETRAN-SP" />
                  </div>
                </div>
              )}

              {activeFormTab === 'contato' && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-700">Contato</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">Telefone</label>
                      <input className="input w-full" value={form.telefone ?? ''} onChange={e => setF('telefone', e.target.value)} placeholder="(xx) xxxxx-xxxx" />
                    </div>
                    <div>
                      <label className="block text-xs font-normal text-slate-500 mb-1">E-mail</label>
                      <input type="email" className="input w-full" value={form.email ?? ''} onChange={e => setF('email', e.target.value)} />
                    </div>
                  </div>
                  <div>
                    <label className="block text-xs font-normal text-slate-500 mb-1">Endereço</label>
                    <input className="input w-full" value={form.endereco ?? ''} onChange={e => setF('endereco', e.target.value)} placeholder="Logradouro, número, bairro, CEP" />
                  </div>
                </div>
              )}

              {activeFormTab === 'lotacao' && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-700">Dados da Unidade</h3>
                  <div>
                    <label className="block text-xs font-normal text-slate-500 mb-1">Unidade</label>
                    <select className="input w-full" value={(form as any).unidade_id ?? ''}
                      onChange={e => { setF('unidade_id', e.target.value ? Number(e.target.value) : null); setF('subunidade_id', null) }}>
                      <option value="">Selecione a unidade...</option>
                      {unidades.filter(u => u.ativa).map(u => (
                        <option key={u.id} value={u.id}>{u.sigla ? `${u.sigla} — ${u.nome}` : u.nome}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-xs font-normal text-slate-500 mb-1">Subunidade</label>
                    <select className="input w-full" value={(form as any).subunidade_id ?? ''}
                      onChange={e => setF('subunidade_id', e.target.value ? Number(e.target.value) : null)}
                      disabled={!(form as any).unidade_id}>
                      <option value="">Selecione a subunidade...</option>
                      {subunidades.filter(s => s.ativa).map(s => (
                        <option key={s.id} value={s.id}>{s.sigla ? `${s.sigla} — ${s.nome}` : s.nome}</option>
                      ))}
                    </select>
                  </div>
                </div>
              )}

              {activeFormTab === 'documentos' && (
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-700">Documentos Anexados</h3>
                  {!editing ? (
                    <p className="text-sm text-slate-500 bg-amber-50 border border-amber-200 rounded-lg px-4 py-3">
                      ⚠️ Salve o condutor primeiro para anexar documentos.
                    </p>
                  ) : (
                    <>
                      <div className="border border-gray-200 rounded-lg p-4 space-y-3">
                        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Adicionar Arquivo</p>
                        <div className="grid grid-cols-2 gap-3">
                          <div>
                            <label className="block text-xs font-normal text-slate-500 mb-1">Tipo</label>
                            <select className="input w-full" value={uploadTipo} onChange={e => setUploadTipo(e.target.value)}>
                              <option value="">Selecione o tipo...</option>
                              <option value="FOTO">Foto</option>
                              <option value="CNH">CNH Digitalizada</option>
                              <option value="OUTRO">Outro</option>
                            </select>
                          </div>
                          <div>
                            <label className="block text-xs font-normal text-slate-500 mb-1">Descrição (opcional)</label>
                            <input className="input w-full" value={uploadDescricao} onChange={e => setUploadDescricao(e.target.value)} placeholder="Ex: CNH frente" />
                          </div>
                        </div>
                        <div>
                          <label className="block text-xs font-normal text-slate-500 mb-1">Arquivo (JPG, PNG, PDF — máx. 10 MB)</label>
                          <input ref={fileInputRef} type="file" accept=".jpg,.jpeg,.png,.pdf,.webp" className="text-sm text-slate-600 w-full"
                            onChange={e => setUploadFile(e.target.files?.[0] ?? null)} />
                        </div>
                        {uploadFile && !uploadTipo && (
                          <p className="text-xs text-amber-600">⚠️ Selecione o Tipo de Documento antes de adicionar.</p>
                        )}
                        <button disabled={!uploadFile || uploadDocMutation.isPending}
                          onClick={() => { if (!uploadFile || !uploadTipo) return; uploadDocMutation.mutate({ tipo: uploadTipo, descricao: uploadDescricao, file: uploadFile }) }}
                          className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors">
                          {uploadDocMutation.isPending ? 'Enviando...' : 'Adicionar Arquivo'}
                        </button>
                      </div>
                      {loadingDocs ? (
                        <p className="text-sm text-slate-400">Carregando documentos...</p>
                      ) : documentos.length === 0 ? (
                        <p className="text-sm text-slate-400 text-center py-4">Nenhum documento anexado.</p>
                      ) : (
                        <div className="space-y-2">
                          {documentos.map(doc => (
                            <div key={doc.id} className="flex items-center gap-3 px-3 py-2 rounded-lg border border-gray-100 bg-gray-50">
                              <span className="text-xl shrink-0">{TIPO_DOC_ICONE[doc.tipo] ?? '📎'}</span>
                              <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-slate-800 truncate">{doc.descricao || TIPO_DOC_LABEL[doc.tipo] || doc.tipo}</p>
                                <p className="text-xs text-slate-400">{TIPO_DOC_LABEL[doc.tipo]} · {new Date(doc.criado_em).toLocaleDateString('pt-BR')}</p>
                              </div>
                              <a href={`/media/${doc.arquivo}`} target="_blank" rel="noreferrer"
                                className="text-xs text-blue-600 hover:text-blue-800 font-medium px-2 py-1 rounded hover:bg-blue-50 transition-colors">
                                Abrir
                              </a>
                              <button onClick={() => deleteDocMutation.mutate(doc.id)}
                                className="text-xs text-red-500 hover:text-red-700 font-medium px-2 py-1 rounded hover:bg-red-50 transition-colors">
                                Remover
                              </button>
                            </div>
                          ))}
                        </div>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>

            <div className="border-t px-6 py-4 flex items-center justify-between shrink-0">
              <div>
                {formError && <p className="text-sm text-red-600">{formError}</p>}
                {successMessage && <p className="text-sm text-green-600">{successMessage}</p>}
              </div>
              <div className="flex gap-3">
                <button onClick={() => setShowForm(false)} className="px-4 py-2 border border-gray-300 text-slate-700 rounded-lg hover:bg-gray-50 text-sm font-medium transition-colors">
                  Cancelar
                </button>
                {activeFormTab !== 'documentos' && (
                  <button onClick={handleSave} disabled={isSaving}
                    className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 text-sm font-medium transition-colors">
                    {isSaving ? 'Salvando...' : editing ? 'Salvar Alterações' : 'Criar Condutor'}
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── Modal de Detalhe ─────────────────────────────────────────────── */}
      {showDetail && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50">
          <div className="bg-white rounded-2xl shadow-2xl w-full max-w-4xl h-[90vh] flex flex-col overflow-hidden">

            <div className="bg-gradient-to-r from-blue-600 to-blue-700 px-8 py-3 text-white shrink-0 relative">
              {!loadingDetail && detailCondutor && (
                <div className="flex items-center justify-between">
                  <div className="flex items-baseline gap-3">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold border ${
                      isAtivo(detailCondutor.status)
                        ? 'bg-green-500/20 text-green-100 border-green-400/40'
                        : detailCondutor.status === 'SUSPENSO'
                          ? 'bg-amber-500/20 text-amber-100 border-amber-400/40'
                          : 'bg-red-500/20 text-red-100 border-red-400/40'
                    }`}>{statusBadge(detailCondutor.status).label}</span>
                    <h2 className="text-3xl font-bold tracking-wide">{detailCondutor.nome}</h2>
                    <p className="text-blue-100 text-sm">Pront. {detailCondutor.prontuario} · {detailCondutor.cargo || 'Condutor'}</p>
                  </div>
                  <button onClick={() => setShowDetail(false)} className="text-white hover:text-gray-200 text-2xl leading-none transition-colors">✕</button>
                </div>
              )}
              {loadingDetail && (
                <div className="flex items-center gap-2 text-blue-100">
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                  <span className="text-sm">Carregando...</span>
                </div>
              )}
            </div>

            <div className="flex-1 overflow-hidden bg-gray-50">
              {loadingDetail ? (
                <div className="flex flex-col items-center justify-center h-full text-gray-400 gap-3">
                  <div className="animate-spin rounded-full h-9 w-9 border-b-2 border-blue-600" />
                  <p className="text-sm">Carregando dados...</p>
                </div>
              ) : detailCondutor ? (
                <div className="h-full flex flex-col p-6 gap-4">

                  <div className="flex gap-4 flex-1 min-h-0">

                    <div className="basis-1/3 shrink-0 flex flex-col gap-3">
                      {(() => {
                        const fotos = detalheDocumentos.filter(d => d.tipo === 'FOTO')
                        const foto = fotos[carouselIdx]
                        return (
                          <div className="relative bg-white rounded-xl border border-gray-200 flex-1 min-h-0 overflow-hidden select-none">
                            {foto ? (
                              <>
                                <img src={`/media/${foto.arquivo}`} alt={foto.descricao || 'Foto'} className="w-full h-full object-cover" />
                                {foto.descricao && (
                                  <div className="absolute bottom-0 left-0 right-0 bg-black/50 text-white text-xs px-2 py-1 text-center truncate">{foto.descricao}</div>
                                )}
                                {fotos.length > 1 && (
                                  <>
                                    <button onClick={() => setCarouselIdx(i => (i - 1 + fotos.length) % fotos.length)}
                                      className="absolute left-1 top-1/2 -translate-y-1/2 bg-black/40 hover:bg-black/70 text-white rounded-full w-7 h-7 flex items-center justify-center text-base leading-none">‹</button>
                                    <button onClick={() => setCarouselIdx(i => (i + 1) % fotos.length)}
                                      className="absolute right-1 top-1/2 -translate-y-1/2 bg-black/40 hover:bg-black/70 text-white rounded-full w-7 h-7 flex items-center justify-center text-base leading-none">›</button>
                                    <div className="absolute top-2 right-2 bg-black/50 text-white text-xs px-1.5 py-0.5 rounded-full">{carouselIdx + 1}/{fotos.length}</div>
                                  </>
                                )}
                              </>
                            ) : (
                              <div className="flex flex-col items-center justify-center h-full gap-2">
                                <span className="text-5xl">👤</span>
                                <p className="text-xs font-normal text-slate-400">Sem fotos</p>
                              </div>
                            )}
                          </div>
                        )
                      })()}

                      <div className="grid grid-cols-2 gap-2">
                        {[
                          { label: 'CPF',        value: detailCondutor.cpf },
                          { label: 'CNH Cat.',   value: detailCondutor.cnh_categoria || '—' },
                          { label: 'Telefone',   value: detailCondutor.telefone || '—' },
                          { label: 'Unidade',    value: detailCondutor.unidade?.sigla || detailCondutor.unidade?.nome || '—' },
                        ].map(({ label, value }) => (
                          <div key={label} className="bg-white rounded-lg px-3 py-2.5 border border-gray-100">
                            <p className="text-xs font-normal text-slate-500">{label}</p>
                            <p className="text-sm font-medium text-slate-800 mt-0.5 truncate">{value}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="flex-1 flex flex-col min-h-0 gap-0">
                      <div className="flex gap-1 border-b border-gray-200 mb-3 shrink-0">
                        {[
                          { id: 'pessoal',    label: 'Pessoal' },
                          { id: 'cnh',        label: 'CNH' },
                          { id: 'contato',    label: 'Contato' },
                          { id: 'lotacao',    label: 'Lotação' },
                          { id: 'documentos', label: 'Documentos' },
                        ].map(tab => (
                          <button key={tab.id} onClick={() => setActiveDetailTab(tab.id)}
                            className={`px-2.5 py-2 text-xs font-semibold border-b-2 transition-colors whitespace-nowrap -mb-px ${
                              activeDetailTab === tab.id ? 'border-blue-600 text-blue-600' : 'border-transparent text-slate-500 hover:text-slate-800'
                            }`}>{tab.label}</button>
                        ))}
                      </div>

                      <div className="bg-white rounded-lg px-4 py-3 flex-1 min-h-0 overflow-y-auto border border-gray-100 no-scrollbar">
                        {activeDetailTab === 'pessoal' && (
                          <div className="space-y-1">
                            <InfoRow label="Nome" value={detailCondutor.nome} />
                            <InfoRow label="Data Nasc." value={fmtDate(detailCondutor.data_nascimento)} />
                            <InfoRow label="CPF" value={detailCondutor.cpf} mono />
                            <InfoRow label="RG" value={detailCondutor.rg} mono />
                            <InfoRow label="Órgão Emissor" value={detailCondutor.orgao_emissor} />
                            <InfoRow label="Cargo" value={detailCondutor.cargo} />
                          </div>
                        )}
                        {activeDetailTab === 'cnh' && (
                          <div className="space-y-1">
                            <InfoRow label="Número CNH" value={detailCondutor.cnh_numero} mono />
                            <InfoRow label="Categoria" value={detailCondutor.cnh_categoria} />
                            <InfoRow label="Emissão" value={fmtDate(detailCondutor.cnh_emissao)} />
                            <InfoRow label="Vencimento" value={fmtDate(detailCondutor.cnh_vencimento)} />
                            <InfoRow label="Órgão Expedidor" value={detailCondutor.cnh_orgao} />
                            {(() => {
                              const b = cnhVencimentoBadge(detailCondutor.cnh_vencimento)
                              return b ? <div className="pt-1"><span className={`px-3 py-1 rounded-full text-xs font-medium ${b.cls}`}>{b.label}</span></div> : null
                            })()}
                          </div>
                        )}
                        {activeDetailTab === 'contato' && (
                          <div className="space-y-1">
                            <InfoRow label="Telefone" value={detailCondutor.telefone} />
                            <InfoRow label="E-mail" value={detailCondutor.email} />
                            <InfoRow label="Endereço" value={detailCondutor.endereco} />
                          </div>
                        )}
                        {activeDetailTab === 'lotacao' && (
                          <div className="space-y-1">
                            <InfoRow label="Unidade" value={detailCondutor.unidade ? `${detailCondutor.unidade.sigla ? detailCondutor.unidade.sigla + ' — ' : ''}${detailCondutor.unidade.nome}` : null} />
                            <InfoRow label="Subunidade" value={detailCondutor.subunidade ? `${detailCondutor.subunidade.sigla ? detailCondutor.subunidade.sigla + ' — ' : ''}${detailCondutor.subunidade.nome}` : null} />
                          </div>
                        )}
                        {activeDetailTab === 'documentos' && (
                          <div className="space-y-4">
                            {(() => {
                              const fotos = detalheDocumentos.filter(d => d.tipo === 'FOTO')
                              return fotos.length > 0 ? (
                                <div>
                                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Fotos ({fotos.length})</p>
                                  <div className="grid grid-cols-3 gap-2">
                                    {fotos.map((doc, idx) => (
                                      <button key={doc.id} onClick={() => setCarouselIdx(idx)}
                                        className={`relative aspect-video rounded-lg overflow-hidden border-2 transition-all ${carouselIdx === idx ? 'border-blue-500 ring-1 ring-blue-300' : 'border-transparent hover:border-blue-300'}`}>
                                        <img src={`/media/${doc.arquivo}`} alt={doc.descricao || 'Foto'} className="w-full h-full object-cover" />
                                        {doc.descricao && (
                                          <div className="absolute bottom-0 inset-x-0 bg-black/50 text-white text-[10px] px-1.5 py-0.5 truncate">{doc.descricao}</div>
                                        )}
                                      </button>
                                    ))}
                                  </div>
                                </div>
                              ) : null
                            })()}
                            {(() => {
                              const outros = detalheDocumentos.filter(d => d.tipo !== 'FOTO')
                              return outros.length > 0 ? (
                                <div>
                                  <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Arquivos ({outros.length})</p>
                                  <div className="space-y-1.5">
                                    {outros.map(doc => (
                                      <a key={doc.id} href={`/media/${doc.arquivo}`} target="_blank" rel="noreferrer"
                                        className="flex items-center gap-3 px-3 py-2 rounded-lg bg-gray-50 hover:bg-blue-50 border border-gray-100 hover:border-blue-200 transition-colors group">
                                        <span className="text-xl shrink-0">{TIPO_DOC_ICONE[doc.tipo] ?? '📎'}</span>
                                        <div className="flex-1 min-w-0">
                                          <p className="text-sm font-medium text-slate-800 truncate">{doc.descricao || TIPO_DOC_LABEL[doc.tipo] || doc.tipo}</p>
                                          <p className="text-xs text-slate-400">{TIPO_DOC_LABEL[doc.tipo]} · {new Date(doc.criado_em).toLocaleDateString('pt-BR')}</p>
                                        </div>
                                        <span className="text-xs text-blue-500 group-hover:text-blue-700 font-medium shrink-0">Abrir →</span>
                                      </a>
                                    ))}
                                  </div>
                                </div>
                              ) : null
                            })()}
                            {detalheDocumentos.length === 0 && (
                              <div className="flex flex-col items-center justify-center h-full gap-2 text-slate-400">
                                <span className="text-3xl">📁</span>
                                <p className="text-sm">Nenhum arquivo anexado</p>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  <div className="grid grid-cols-3 gap-3 shrink-0">
                    {[
                      { label: 'CNH Vencimento', value: fmtDate(detailCondutor.cnh_vencimento) },
                      { label: 'CNH Emissão',    value: fmtDate(detailCondutor.cnh_emissao) },
                      { label: 'Unidade',        value: detailCondutor.unidade?.nome || '—' },
                    ].map(({ label, value }) => (
                      <div key={label} className="bg-white rounded-lg px-4 py-3 border border-gray-100">
                        <p className="text-xs font-normal text-slate-500">{label}</p>
                        <p className="text-sm font-medium text-slate-800 mt-0.5">{value}</p>
                      </div>
                    ))}
                  </div>
                </div>
              ) : null}
            </div>

            <div className="border-t px-6 py-4 flex justify-end gap-3 bg-white shrink-0">
              {detailCondutor && (
                <button onClick={() => { setShowDetail(false); openEdit(detailCondutor) }}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm font-medium transition-colors">
                  ✏️ Editar
                </button>
              )}
              <button onClick={() => setShowDetail(false)}
                className="px-4 py-2 border border-gray-300 text-slate-700 rounded-lg hover:bg-gray-50 text-sm font-medium transition-colors">
                Fechar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
