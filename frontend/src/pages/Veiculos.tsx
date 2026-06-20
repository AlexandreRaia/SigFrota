'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { veiculoService } from '@/services/veiculos'
import { Button } from '@/components/ui/Button'
import type { Veiculo, VeiculoListItem } from '@/types'

const TABS = [
  { id: 'gerais', label: '📋 Dados Gerais' },
  { id: 'classificacao', label: '🏷️ Classificação' },
  { id: 'administrativa', label: '🏢 Administrativa' },
  { id: 'operacional', label: '⚙️ Operacional' },
  { id: 'documentacao', label: '📄 Documentação' },
]

export default function Veiculos() {
  const [q, setQ] = useState('')
  const [situacao, setSituacao] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [activeTab, setActiveTab] = useState('gerais')
  const [editing, setEditing] = useState<Veiculo | null>(null)
  const [formError, setFormError] = useState<string | null>(null)
  const [successMessage, setSuccessMessage] = useState<string | null>(null)

  // Queries
  const { data: veiculos, isLoading } = useQuery({
    queryKey: ['veiculos', { q, situacao }],
    queryFn: () => veiculoService.listar({ q, situacao }),
  })

  const { data: categorias } = useQuery({
    queryKey: ['veiculos', 'categorias'],
    queryFn: () => veiculoService.categorias(),
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
    uf: 'SP',
    situacao: 'ATIVA',
    tipo_controle: 'QUILOMETRAGEM',
    hodometro_horimetro_inicial: 0,
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

  function openCreate() {
    setEditing(null)
    setForm({
      placa: '',
      prefixo: '',
      chassi: '',
      renavam: '',
      ano_fabricacao: new Date().getFullYear(),
      combustivel: 'FLEX',
      uf: 'SP',
      situacao: 'ATIVA',
      tipo_controle: 'QUILOMETRAGEM',
      hodometro_horimetro_inicial: 0,
    })
    setMarcaId(null)
    setActiveTab('gerais')
    setShowForm(true)
  }

  async function openEdit(v: VeiculoListItem) {
    const full = await veiculoService.detalhe(v.id)
    setEditing(full)
    setForm(full)
    setMarcaId(full.marca?.id || null)
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
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700">Categoria</th>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-700">Combustível</th>
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
                  <td className="px-6 py-3 text-gray-600">{v.categoria?.nome || '—'}</td>
                  <td className="px-6 py-3 text-gray-600">{v.combustivel}</td>
                  <td className="px-6 py-3">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium ${v.situacao === 'ATIVA' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                      {v.situacao}
                    </span>
                  </td>
                  <td className="px-6 py-3 text-sm space-x-2">
                    <button onClick={() => openEdit(v)} className="text-blue-600 hover:text-blue-900 font-medium">
                      Editar
                    </button>
                    <button onClick={() => handleDelete(v.id)} className="text-red-600 hover:text-red-900 font-medium">
                      Excluir
                    </button>
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
          <div className="bg-white rounded-lg shadow-xl w-full max-w-5xl h-[90vh] flex flex-col">
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
                  className={`px-4 py-3 whitespace-nowrap border-b-2 transition-colors ${
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
            <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
              {/* 📋 Dados Gerais */}
              {activeTab === 'gerais' && (
                <div className="bg-white rounded-lg p-6 space-y-4">
                  <h3 className="font-bold text-lg mb-4">Informações do Veículo</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Placa *</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.placa || ''}
                        onChange={(e) => setForm({ ...form, placa: e.target.value.toUpperCase() })}
                        placeholder="ABC-1234"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Prefixo *</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.prefixo || ''}
                        onChange={(e) => setForm({ ...form, prefixo: e.target.value })}
                        placeholder="V-001"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Chassi *</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.chassi || ''}
                        onChange={(e) => setForm({ ...form, chassi: e.target.value.toUpperCase() })}
                        placeholder="17 caracteres"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">RENAVAM *</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.renavam || ''}
                        onChange={(e) => setForm({ ...form, renavam: e.target.value.replace(/\D/g, '') })}
                        placeholder="11 dígitos"
                      />
                    </div>
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

              {/* 🏷️ Classificação */}
              {activeTab === 'classificacao' && (
                <div className="bg-white rounded-lg p-6 space-y-4">
                  <h3 className="font-bold text-lg mb-4">Classificação do Veículo</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Categoria</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.categoria_id || ''}
                        onChange={(e) => setForm({ ...form, categoria_id: e.target.value ? parseInt(e.target.value) : undefined })}
                      >
                        <option value="">Selecione...</option>
                        {categorias?.map((c) => (
                          <option key={c.id} value={c.id}>{c.nome}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Tipo Frota</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.tipo_frota_id || ''}
                        onChange={(e) => setForm({ ...form, tipo_frota_id: e.target.value ? parseInt(e.target.value) : undefined })}
                      >
                        <option value="">Selecione...</option>
                        {tiposFrota?.map((t) => (
                          <option key={t.id} value={t.id}>{t.nome}</option>
                        ))}
                      </select>
                    </div>
                  </div>
                </div>
              )}

              {/* 🏢 Administrativa */}
              {activeTab === 'administrativa' && (
                <div className="bg-white rounded-lg p-6 space-y-4">
                  <h3 className="font-bold text-lg mb-4">Dados Administrativos</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">Secretaria</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        disabled
                      >
                        <option value="">Padrão</option>
                      </select>
                      <p className="text-xs text-gray-500 mt-1">Vinculado ao usuário</p>
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
                    <div>
                      <label className="block text-sm font-medium mb-1">Centro de Custo</label>
                      <select
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.centro_custo_id || ''}
                        onChange={(e) => setForm({ ...form, centro_custo_id: e.target.value ? parseInt(e.target.value) : undefined })}
                      >
                        <option value="">Selecione...</option>
                        {centrosCusto?.map((cc) => (
                          <option key={cc.id} value={cc.id}>{cc.codigo} - {cc.descricao}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Estado (UF)</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.uf || 'SP'}
                        onChange={(e) => setForm({ ...form, uf: e.target.value.toUpperCase() })}
                        maxLength={2}
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-1">Município</label>
                      <input
                        type="text"
                        className="w-full px-3 py-2 border rounded-lg"
                        value={form.municipio || ''}
                        onChange={(e) => setForm({ ...form, municipio: e.target.value })}
                        placeholder="Ex: São Paulo"
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
                <div className="bg-white rounded-lg p-6 space-y-4">
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
    </div>
  )
}
