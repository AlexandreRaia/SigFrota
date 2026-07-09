'use client'

import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { FiPlus, FiEdit2, FiPower, FiTrash2 } from 'react-icons/fi'
import { Button } from '@/components/ui/Button'
import {
  parametrizacaoService,
  type UnidadePayload,
  type SubunidadePayload,
  type CentroCustoPayload,
} from '@/services/parametrizacoes'
import type { Unidade, Subunidade, CentroCusto } from '@/types'

type Aba =
  | 'unidades'
  | 'setores'
  | 'centros'
  | 'tipos-frota'
  | 'categorias'
  | 'tipos-veiculo'
  | 'marcas'
  | 'modelos'
  | 'combustiveis'

const statusBadge = (ativa: boolean) =>
  ativa ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'

export default function Parametrizacoes() {
  const queryClient = useQueryClient()
  const [aba, setAba] = useState<Aba>('unidades')

  const { data: unidades = [], isPending: loadingUnidades } = useQuery({
    queryKey: ['param-unidades'],
    queryFn: () => parametrizacaoService.listarUnidades(),
  })

  const { data: setores = [], isPending: loadingSetores } = useQuery({
    queryKey: ['param-subunidades'],
    queryFn: () => parametrizacaoService.listarSubunidades(),
  })

  const { data: centros = [], isPending: loadingCentros } = useQuery({
    queryKey: ['param-centros-custo'],
    queryFn: () => parametrizacaoService.listarCentrosCusto(),
  })

  // Marcas usadas tanto na aba "Marcas" quanto como opções da aba "Modelos".
  const { data: marcasList = [] } = useQuery({
    queryKey: ['param-marcas'],
    queryFn: () => parametrizacaoService.listarMarcas(),
  })

  const unidadeNome = (id: number | null) =>
    unidades.find((u) => u.id === id)?.nome ?? '—'

  // ── Estado dos modais ──────────────────────────────────────────────────────
  const [showUnidade, setShowUnidade] = useState(false)
  const [editUnidade, setEditUnidade] = useState<Unidade | null>(null)
  const [showSetor, setShowSetor] = useState(false)
  const [editSetor, setEditSetor] = useState<Subunidade | null>(null)
  const [showCentro, setShowCentro] = useState(false)
  const [editCentro, setEditCentro] = useState<CentroCusto | null>(null)

  // ── Mutations Unidade ──────────────────────────────────────────────────────
  const invalidateUnidades = () =>
    queryClient.invalidateQueries({ queryKey: ['param-unidades'] })
  const invalidateSetores = () =>
    queryClient.invalidateQueries({ queryKey: ['param-subunidades'] })

  const salvarUnidade = useMutation({
    mutationFn: (payload: { id?: number; data: UnidadePayload }) =>
      payload.id
        ? parametrizacaoService.atualizarUnidade(payload.id, payload.data)
        : parametrizacaoService.criarUnidade(payload.data),
    onSuccess: () => {
      invalidateUnidades()
      setShowUnidade(false)
      setEditUnidade(null)
    },
  })

  const toggleUnidade = useMutation({
    mutationFn: (u: Unidade) =>
      parametrizacaoService.atualizarUnidade(u.id, { ativa: !u.ativa }),
    onSuccess: invalidateUnidades,
  })

  const excluirUnidade = useMutation({
    mutationFn: (id: number) => parametrizacaoService.excluirUnidade(id),
    onSuccess: invalidateUnidades,
    onError: (err: any) =>
      alert(err?.response?.data?.detail || 'Erro ao excluir unidade'),
  })

  // ── Mutations Setor/Departamento ───────────────────────────────────────────
  const salvarSetor = useMutation({
    mutationFn: (payload: { id?: number; data: SubunidadePayload }) =>
      payload.id
        ? parametrizacaoService.atualizarSubunidade(payload.id, payload.data)
        : parametrizacaoService.criarSubunidade(payload.data),
    onSuccess: () => {
      invalidateSetores()
      setShowSetor(false)
      setEditSetor(null)
    },
  })

  const toggleSetor = useMutation({
    mutationFn: (s: Subunidade) =>
      parametrizacaoService.atualizarSubunidade(s.id, { ativa: !s.ativa }),
    onSuccess: invalidateSetores,
  })

  const excluirSetor = useMutation({
    mutationFn: (id: number) => parametrizacaoService.excluirSubunidade(id),
    onSuccess: invalidateSetores,
    onError: (err: any) =>
      alert(err?.response?.data?.detail || 'Erro ao excluir setor/departamento'),
  })

  // ── Mutations Centro de Custo ──────────────────────────────────────────────
  const invalidateCentros = () =>
    queryClient.invalidateQueries({ queryKey: ['param-centros-custo'] })

  const salvarCentro = useMutation({
    mutationFn: (payload: { id?: number; data: CentroCustoPayload }) =>
      payload.id
        ? parametrizacaoService.atualizarCentroCusto(payload.id, payload.data)
        : parametrizacaoService.criarCentroCusto(payload.data),
    onSuccess: () => {
      invalidateCentros()
      setShowCentro(false)
      setEditCentro(null)
    },
  })

  const toggleCentro = useMutation({
    mutationFn: (c: CentroCusto) =>
      parametrizacaoService.atualizarCentroCusto(c.id, { ativa: !c.ativa }),
    onSuccess: invalidateCentros,
  })

  const excluirCentro = useMutation({
    mutationFn: (id: number) => parametrizacaoService.excluirCentroCusto(id),
    onSuccess: invalidateCentros,
    onError: (err: any) =>
      alert(err?.response?.data?.detail || 'Erro ao excluir centro de custo'),
  })

  return (
    <div className="space-y-4 p-6">
      {/* Cabeçalho */}
      <div>
        <h1 className="text-xl font-bold text-slate-800">🏢 Parametrizações</h1>
      </div>

      {/* Abas */}
      <div className="flex gap-2 border-b border-gray-200">
        {([
          { id: 'unidades', label: 'Unidades' },
          { id: 'setores', label: 'Setores / Departamentos' },
          { id: 'centros', label: 'Centros de Custo' },
          { id: 'tipos-frota', label: 'Tipos de Frota' },
          { id: 'categorias', label: 'Categorias' },
          { id: 'tipos-veiculo', label: 'Tipos de Veículo' },
          { id: 'marcas', label: 'Marcas' },
          { id: 'modelos', label: 'Modelos' },
          { id: 'combustiveis', label: 'Combustíveis' },
        ] as { id: Aba; label: string }[]).map((t) => (
          <button
            key={t.id}
            onClick={() => setAba(t.id)}
            className={`px-4 py-2 text-sm font-medium -mb-px border-b-2 transition-colors ${
              aba === t.id
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700'
            }`}
          >
            {t.label}
          </button>
        ))}
      </div>

      {/* ── Aba Unidades ──────────────────────────────────────────────────── */}
      {aba === 'unidades' && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <Button
              onClick={() => { setEditUnidade(null); setShowUnidade(true) }}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <span className="flex items-center gap-2">
                <FiPlus /> Nova Unidade
              </span>
            </Button>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Nome</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Sigla</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Situação</th>
                  <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-500">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 bg-white">
                {loadingUnidades ? (
                  <tr><td colSpan={4} className="px-6 py-8 text-center text-gray-400">Carregando...</td></tr>
                ) : unidades.length === 0 ? (
                  <tr><td colSpan={4} className="px-6 py-8 text-center text-gray-400">Nenhuma unidade cadastrada.</td></tr>
                ) : (
                  unidades.map((u) => (
                    <tr key={u.id} className="hover:bg-gray-50">
                      <td className="px-6 py-3 text-sm text-gray-800">{u.nome}</td>
                      <td className="px-6 py-3 text-sm text-slate-500">{u.sigla || '—'}</td>
                      <td className="px-6 py-3">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${statusBadge(u.ativa)}`}>
                          {u.ativa ? 'Ativa' : 'Inativa'}
                        </span>
                      </td>
                      <td className="px-6 py-3">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => { setEditUnidade(u); setShowUnidade(true) }}
                            className="text-gray-500 hover:text-blue-600"
                            title="Editar"
                          >
                            <FiEdit2 />
                          </button>
                          <button
                            onClick={() => toggleUnidade.mutate(u)}
                            className={u.ativa ? 'text-gray-500 hover:text-red-600' : 'text-gray-500 hover:text-green-600'}
                            title={u.ativa ? 'Inativar' : 'Ativar'}
                          >
                            <FiPower />
                          </button>
                          <button
                            onClick={() => {
                              if (window.confirm(`Excluir a unidade "${u.nome}"?`)) excluirUnidade.mutate(u.id)
                            }}
                            className="text-gray-500 hover:text-red-600"
                            title="Excluir"
                          >
                            <FiTrash2 />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ── Aba Setores/Departamentos ─────────────────────────────────────── */}
      {aba === 'setores' && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <Button
              onClick={() => { setEditSetor(null); setShowSetor(true) }}
              className="bg-blue-600 hover:bg-blue-700"
              disabled={unidades.length === 0}
            >
              <span className="flex items-center gap-2">
                <FiPlus /> Novo Setor/Departamento
              </span>
            </Button>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Nome</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Sigla</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Unidade</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Situação</th>
                  <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-500">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 bg-white">
                {loadingSetores ? (
                  <tr><td colSpan={5} className="px-6 py-8 text-center text-gray-400">Carregando...</td></tr>
                ) : setores.length === 0 ? (
                  <tr><td colSpan={5} className="px-6 py-8 text-center text-gray-400">Nenhum setor/departamento cadastrado.</td></tr>
                ) : (
                  setores.map((s) => (
                    <tr key={s.id} className="hover:bg-gray-50">
                      <td className="px-6 py-3 text-sm text-gray-800">{s.nome}</td>
                      <td className="px-6 py-3 text-sm text-slate-500">{s.sigla || '—'}</td>
                      <td className="px-6 py-3 text-sm text-slate-500">{unidadeNome(s.unidade_id)}</td>
                      <td className="px-6 py-3">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${statusBadge(s.ativa)}`}>
                          {s.ativa ? 'Ativa' : 'Inativa'}
                        </span>
                      </td>
                      <td className="px-6 py-3">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => { setEditSetor(s); setShowSetor(true) }}
                            className="text-gray-500 hover:text-blue-600"
                            title="Editar"
                          >
                            <FiEdit2 />
                          </button>
                          <button
                            onClick={() => toggleSetor.mutate(s)}
                            className={s.ativa ? 'text-gray-500 hover:text-red-600' : 'text-gray-500 hover:text-green-600'}
                            title={s.ativa ? 'Inativar' : 'Ativar'}
                          >
                            <FiPower />
                          </button>
                          <button
                            onClick={() => {
                              if (window.confirm(`Excluir o setor/departamento "${s.nome}"?`)) excluirSetor.mutate(s.id)
                            }}
                            className="text-gray-500 hover:text-red-600"
                            title="Excluir"
                          >
                            <FiTrash2 />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ── Aba Centros de Custo ──────────────────────────────────────────── */}
      {aba === 'centros' && (
        <div className="space-y-4">
          <div className="flex justify-end">
            <Button
              onClick={() => { setEditCentro(null); setShowCentro(true) }}
              className="bg-blue-600 hover:bg-blue-700"
            >
              <span className="flex items-center gap-2">
                <FiPlus /> Novo Centro de Custo
              </span>
            </Button>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            <table className="w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Código</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Nome</th>
                  <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Situação</th>
                  <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-500">Ações</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 bg-white">
                {loadingCentros ? (
                  <tr><td colSpan={4} className="px-6 py-8 text-center text-gray-400">Carregando...</td></tr>
                ) : centros.length === 0 ? (
                  <tr><td colSpan={4} className="px-6 py-8 text-center text-gray-400">Nenhum centro de custo cadastrado.</td></tr>
                ) : (
                  centros.map((c) => (
                    <tr key={c.id} className="hover:bg-gray-50">
                      <td className="px-6 py-3 text-sm text-gray-800">{c.codigo}</td>
                      <td className="px-6 py-3 text-sm text-slate-500">{c.nome}</td>
                      <td className="px-6 py-3">
                        <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${statusBadge(c.ativa)}`}>
                          {c.ativa ? 'Ativa' : 'Inativa'}
                        </span>
                      </td>
                      <td className="px-6 py-3">
                        <div className="flex items-center justify-end gap-2">
                          <button
                            onClick={() => { setEditCentro(c); setShowCentro(true) }}
                            className="text-gray-500 hover:text-blue-600"
                            title="Editar"
                          >
                            <FiEdit2 />
                          </button>
                          <button
                            onClick={() => toggleCentro.mutate(c)}
                            className={c.ativa ? 'text-gray-500 hover:text-red-600' : 'text-gray-500 hover:text-green-600'}
                            title={c.ativa ? 'Inativar' : 'Ativar'}
                          >
                            <FiPower />
                          </button>
                          <button
                            onClick={() => {
                              if (window.confirm(`Excluir o centro de custo "${c.codigo} - ${c.nome}"?`)) excluirCentro.mutate(c.id)
                            }}
                            className="text-gray-500 hover:text-red-600"
                            title="Excluir"
                          >
                            <FiTrash2 />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* ── Aba Tipos de Frota ────────────────────────────────────────────── */}
      {aba === 'tipos-frota' && (
        <LookupCrud
          config={{
            singular: 'Tipo de Frota',
            novoLabel: 'Novo Tipo de Frota',
            queryKey: 'param-tipos-frota',
            list: parametrizacaoService.listarTiposFrota,
            create: parametrizacaoService.criarTipoFrota,
            update: parametrizacaoService.atualizarTipoFrota,
            remove: parametrizacaoService.excluirTipoFrota,
          }}
        />
      )}

      {/* ── Aba Categorias ────────────────────────────────────────────────── */}
      {aba === 'categorias' && (
        <LookupCrud
          config={{
            singular: 'Categoria',
            novoLabel: 'Nova Categoria',
            queryKey: 'param-categorias',
            hasDescricao: true,
            list: parametrizacaoService.listarCategorias,
            create: parametrizacaoService.criarCategoria,
            update: parametrizacaoService.atualizarCategoria,
            remove: parametrizacaoService.excluirCategoria,
          }}
        />
      )}

      {/* ── Aba Tipos de Veículo ──────────────────────────────────────────── */}
      {aba === 'tipos-veiculo' && (
        <LookupCrud
          config={{
            singular: 'Tipo de Veículo',
            novoLabel: 'Novo Tipo de Veículo',
            queryKey: 'param-tipos-veiculo',
            list: parametrizacaoService.listarTiposVeiculo,
            create: parametrizacaoService.criarTipoVeiculo,
            update: parametrizacaoService.atualizarTipoVeiculo,
            remove: parametrizacaoService.excluirTipoVeiculo,
          }}
        />
      )}

      {/* ── Aba Marcas ────────────────────────────────────────────────────── */}
      {aba === 'marcas' && (
        <LookupCrud
          config={{
            singular: 'Marca',
            novoLabel: 'Nova Marca',
            queryKey: 'param-marcas',
            list: parametrizacaoService.listarMarcas,
            create: parametrizacaoService.criarMarca,
            update: parametrizacaoService.atualizarMarca,
            remove: parametrizacaoService.excluirMarca,
          }}
        />
      )}

      {/* ── Aba Modelos ───────────────────────────────────────────────────── */}
      {aba === 'modelos' && (
        <LookupCrud
          config={{
            singular: 'Modelo',
            novoLabel: 'Novo Modelo',
            queryKey: 'param-modelos',
            list: parametrizacaoService.listarModelos,
            create: parametrizacaoService.criarModelo,
            update: parametrizacaoService.atualizarModelo,
            remove: parametrizacaoService.excluirModelo,
            parent: { label: 'Marca', options: marcasList },
          }}
        />
      )}

      {/* ── Aba Combustíveis ──────────────────────────────────────────────── */}
      {aba === 'combustiveis' && (
        <LookupCrud
          config={{
            singular: 'Combustível',
            novoLabel: 'Novo Combustível',
            queryKey: 'param-combustiveis',
            list: parametrizacaoService.listarCombustiveis,
            create: parametrizacaoService.criarCombustivel,
            update: parametrizacaoService.atualizarCombustivel,
            remove: parametrizacaoService.excluirCombustivel,
          }}
        />
      )}

      {/* ── Modal Unidade ─────────────────────────────────────────────────── */}
      {showUnidade && (
        <UnidadeModal
          unidade={editUnidade}
          isSaving={salvarUnidade.isPending}
          error={(salvarUnidade.error as any)?.response?.data?.detail}
          onClose={() => { setShowUnidade(false); setEditUnidade(null); salvarUnidade.reset() }}
          onSave={(data) => salvarUnidade.mutate({ id: editUnidade?.id, data })}
        />
      )}

      {/* ── Modal Setor/Departamento ──────────────────────────────────────── */}
      {showSetor && (
        <SetorModal
          setor={editSetor}
          unidades={unidades}
          isSaving={salvarSetor.isPending}
          error={(salvarSetor.error as any)?.response?.data?.detail}
          onClose={() => { setShowSetor(false); setEditSetor(null); salvarSetor.reset() }}
          onSave={(data) => salvarSetor.mutate({ id: editSetor?.id, data })}
        />
      )}

      {/* ── Modal Centro de Custo ─────────────────────────────────────────── */}
      {showCentro && (
        <CentroCustoModal
          centro={editCentro}
          isSaving={salvarCentro.isPending}
          error={(salvarCentro.error as any)?.response?.data?.detail}
          onClose={() => { setShowCentro(false); setEditCentro(null); salvarCentro.reset() }}
          onSave={(data) => salvarCentro.mutate({ id: editCentro?.id, data })}
        />
      )}
    </div>
  )
}

// ── Modal de Unidade ──────────────────────────────────────────────────────────

function UnidadeModal({
  unidade,
  isSaving,
  error,
  onClose,
  onSave,
}: {
  unidade: Unidade | null
  isSaving: boolean
  error?: string
  onClose: () => void
  onSave: (data: UnidadePayload) => void
}) {
  const [nome, setNome] = useState(unidade?.nome ?? '')
  const [sigla, setSigla] = useState(unidade?.sigla ?? '')
  const [ativa, setAtiva] = useState(unidade?.ativa ?? true)
  const [localError, setLocalError] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!nome.trim()) return setLocalError('Nome é obrigatório')
    onSave({ nome: nome.trim(), sigla: sigla.trim(), ativa })
  }

  return (
    <ModalShell title={unidade ? 'Editar Unidade' : 'Nova Unidade'} onClose={onClose}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Field label="Nome (ex: Secretaria de Administração)">
          <input className="input" value={nome} onChange={(e) => setNome(e.target.value)} autoFocus />
        </Field>
        <Field label="Sigla (ex: SMA)">
          <input className="input" value={sigla} maxLength={20} onChange={(e) => setSigla(e.target.value)} />
        </Field>
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" checked={ativa} onChange={(e) => setAtiva(e.target.checked)} />
          Ativa
        </label>

        {(localError || error) && (
          <p className="text-sm text-red-600">{localError || error}</p>
        )}

        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button type="submit" isLoading={isSaving} className="bg-blue-600 hover:bg-blue-700">Salvar</Button>
        </div>
      </form>
    </ModalShell>
  )
}

// ── Modal de Setor/Departamento ───────────────────────────────────────────────

function SetorModal({
  setor,
  unidades,
  isSaving,
  error,
  onClose,
  onSave,
}: {
  setor: Subunidade | null
  unidades: Unidade[]
  isSaving: boolean
  error?: string
  onClose: () => void
  onSave: (data: SubunidadePayload) => void
}) {
  const [nome, setNome] = useState(setor?.nome ?? '')
  const [sigla, setSigla] = useState(setor?.sigla ?? '')
  const [unidadeId, setUnidadeId] = useState<number | ''>(setor?.unidade_id ?? '')
  const [ativa, setAtiva] = useState(setor?.ativa ?? true)
  const [localError, setLocalError] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!nome.trim()) return setLocalError('Nome é obrigatório')
    if (!unidadeId) return setLocalError('Unidade é obrigatória')
    onSave({ nome: nome.trim(), sigla: sigla.trim(), unidade_id: Number(unidadeId), ativa })
  }

  return (
    <ModalShell title={setor ? 'Editar Setor/Departamento' : 'Novo Setor/Departamento'} onClose={onClose}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Field label="Unidade (Secretaria)">
          <select
            className="input"
            value={unidadeId}
            onChange={(e) => setUnidadeId(e.target.value ? Number(e.target.value) : '')}
          >
            <option value="">Selecione...</option>
            {unidades.filter((u) => u.ativa).map((u) => (
              <option key={u.id} value={u.id}>{u.nome}</option>
            ))}
          </select>
        </Field>
        <Field label="Nome (ex: Departamento de Transportes)">
          <input className="input" value={nome} onChange={(e) => setNome(e.target.value)} autoFocus />
        </Field>
        <Field label="Sigla (ex: DTR)">
          <input className="input" value={sigla} maxLength={20} onChange={(e) => setSigla(e.target.value)} />
        </Field>
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" checked={ativa} onChange={(e) => setAtiva(e.target.checked)} />
          Ativa
        </label>

        {(localError || error) && (
          <p className="text-sm text-red-600">{localError || error}</p>
        )}

        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button type="submit" isLoading={isSaving} className="bg-blue-600 hover:bg-blue-700">Salvar</Button>
        </div>
      </form>
    </ModalShell>
  )
}

// ── Modal de Centro de Custo ───────────────────────────────────────────────────

function CentroCustoModal({
  centro,
  isSaving,
  error,
  onClose,
  onSave,
}: {
  centro: CentroCusto | null
  isSaving: boolean
  error?: string
  onClose: () => void
  onSave: (data: CentroCustoPayload) => void
}) {
  const [codigo, setCodigo] = useState(centro?.codigo ?? '')
  const [nome, setNome] = useState(centro?.nome ?? '')
  const [ativa, setAtiva] = useState(centro?.ativa ?? true)
  const [localError, setLocalError] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!codigo.trim()) return setLocalError('Código é obrigatório')
    if (!nome.trim()) return setLocalError('Nome é obrigatório')
    onSave({ codigo: codigo.trim(), nome: nome.trim(), ativa })
  }

  return (
    <ModalShell title={centro ? 'Editar Centro de Custo' : 'Novo Centro de Custo'} onClose={onClose}>
      <form onSubmit={handleSubmit} className="space-y-4">
        <Field label="Código (ex: 001)">
          <input className="input" value={codigo} maxLength={20} onChange={(e) => setCodigo(e.target.value)} autoFocus />
        </Field>
        <Field label="Nome (ex: Transporte Escolar)">
          <input className="input" value={nome} onChange={(e) => setNome(e.target.value)} />
        </Field>
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" checked={ativa} onChange={(e) => setAtiva(e.target.checked)} />
          Ativa
        </label>

        {(localError || error) && (
          <p className="text-sm text-red-600">{localError || error}</p>
        )}

        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button type="submit" isLoading={isSaving} className="bg-blue-600 hover:bg-blue-700">Salvar</Button>
        </div>
      </form>
    </ModalShell>
  )
}

// ── Componentes auxiliares ────────────────────────────────────────────────────

function ModalShell({
  title,
  onClose,
  children,
}: {
  title: string
  onClose: () => void
  children: React.ReactNode
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4" onClick={onClose}>
      <div
        className="w-full max-w-md rounded-2xl bg-white shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between border-b border-gray-100 px-6 py-4">
          <h2 className="text-base font-semibold text-slate-800">{title}</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600" aria-label="Fechar">✕</button>
        </div>
        <div className="p-6">{children}</div>
      </div>
    </div>
  )
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="space-y-1">
      <label className="text-xs font-normal text-slate-500">{label}</label>
      {children}
    </div>
  )
}

// ── CRUD genérico para tabelas de apoio (Selects) ─────────────────────────────

type LookupRow = {
  id: number
  nome: string
  ativo: boolean
  descricao?: string
  marca_id?: number
}

type LookupPayloadData = {
  nome: string
  ativo: boolean
  descricao?: string
  marca_id?: number
}

interface LookupCrudConfig {
  singular: string
  novoLabel: string
  queryKey: string
  list: () => Promise<LookupRow[]>
  create: (data: LookupPayloadData) => Promise<void>
  update: (id: number, data: Partial<LookupPayloadData>) => Promise<void>
  remove: (id: number) => Promise<void>
  hasDescricao?: boolean
  parent?: { label: string; options: { id: number; nome: string }[] }
}

function LookupCrud({ config }: { config: LookupCrudConfig }) {
  const queryClient = useQueryClient()
  const [showModal, setShowModal] = useState(false)
  const [editing, setEditing] = useState<LookupRow | null>(null)

  const { data: itens = [], isPending } = useQuery({
    queryKey: [config.queryKey],
    queryFn: config.list,
  })

  const invalidate = () =>
    queryClient.invalidateQueries({ queryKey: [config.queryKey] })

  const salvar = useMutation({
    mutationFn: (payload: { id?: number; data: LookupPayloadData }) =>
      payload.id ? config.update(payload.id, payload.data) : config.create(payload.data),
    onSuccess: () => { invalidate(); setShowModal(false); setEditing(null) },
  })

  const toggle = useMutation({
    mutationFn: (row: LookupRow) => config.update(row.id, { ativo: !row.ativo }),
    onSuccess: invalidate,
  })

  const excluir = useMutation({
    mutationFn: (id: number) => config.remove(id),
    onSuccess: invalidate,
    onError: (err: any) =>
      alert(err?.response?.data?.detail || `Erro ao excluir ${config.singular.toLowerCase()}.`),
  })

  const parentName = (id?: number) =>
    config.parent?.options.find((o) => o.id === id)?.nome ?? '—'

  const colSpan = 2 + (config.hasDescricao ? 1 : 0) + (config.parent ? 1 : 0) + 1
  const semMarcas = !!config.parent && config.parent.options.length === 0

  return (
    <div className="space-y-4">
      <div className="flex justify-end">
        <Button
          onClick={() => { setEditing(null); setShowModal(true) }}
          disabled={semMarcas}
          className="bg-blue-600 hover:bg-blue-700"
        >
          <span className="flex items-center gap-2">
            <FiPlus /> {config.novoLabel}
          </span>
        </Button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Nome</th>
              {config.hasDescricao && (
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Descrição</th>
              )}
              {config.parent && (
                <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">{config.parent.label}</th>
              )}
              <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-slate-500">Situação</th>
              <th className="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-slate-500">Ações</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 bg-white">
            {isPending ? (
              <tr><td colSpan={colSpan} className="px-6 py-8 text-center text-gray-400">Carregando...</td></tr>
            ) : itens.length === 0 ? (
              <tr><td colSpan={colSpan} className="px-6 py-8 text-center text-gray-400">Nenhum registro cadastrado.</td></tr>
            ) : (
              itens.map((row) => (
                <tr key={row.id} className="hover:bg-gray-50">
                  <td className="px-6 py-3 text-sm text-gray-800">{row.nome}</td>
                  {config.hasDescricao && (
                    <td className="px-6 py-3 text-sm text-slate-500">{row.descricao || '—'}</td>
                  )}
                  {config.parent && (
                    <td className="px-6 py-3 text-sm text-slate-500">{parentName(row.marca_id)}</td>
                  )}
                  <td className="px-6 py-3">
                    <span className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${statusBadge(row.ativo)}`}>
                      {row.ativo ? 'Ativo' : 'Inativo'}
                    </span>
                  </td>
                  <td className="px-6 py-3">
                    <div className="flex items-center justify-end gap-2">
                      <button
                        onClick={() => { setEditing(row); setShowModal(true) }}
                        className="text-gray-500 hover:text-blue-600"
                        title="Editar"
                      >
                        <FiEdit2 />
                      </button>
                      <button
                        onClick={() => toggle.mutate(row)}
                        className={row.ativo ? 'text-gray-500 hover:text-red-600' : 'text-gray-500 hover:text-green-600'}
                        title={row.ativo ? 'Inativar' : 'Ativar'}
                      >
                        <FiPower />
                      </button>
                      <button
                        onClick={() => {
                          if (window.confirm(`Excluir "${row.nome}"?`)) excluir.mutate(row.id)
                        }}
                        className="text-gray-500 hover:text-red-600"
                        title="Excluir"
                      >
                        <FiTrash2 />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <LookupModal
          config={config}
          row={editing}
          isSaving={salvar.isPending}
          error={(salvar.error as any)?.response?.data?.detail}
          onClose={() => { setShowModal(false); setEditing(null); salvar.reset() }}
          onSave={(data) => salvar.mutate({ id: editing?.id, data })}
        />
      )}
    </div>
  )
}

function LookupModal({
  config,
  row,
  isSaving,
  error,
  onClose,
  onSave,
}: {
  config: LookupCrudConfig
  row: LookupRow | null
  isSaving: boolean
  error?: string
  onClose: () => void
  onSave: (data: LookupPayloadData) => void
}) {
  const [nome, setNome] = useState(row?.nome ?? '')
  const [descricao, setDescricao] = useState(row?.descricao ?? '')
  const [marcaId, setMarcaId] = useState<number | ''>(row?.marca_id ?? '')
  const [ativo, setAtivo] = useState(row?.ativo ?? true)
  const [localError, setLocalError] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!nome.trim()) return setLocalError('Nome é obrigatório')
    if (config.parent && !marcaId) return setLocalError(`${config.parent.label} é obrigatória`)

    const data: LookupPayloadData = { nome: nome.trim(), ativo }
    if (config.hasDescricao) data.descricao = descricao.trim()
    if (config.parent) data.marca_id = Number(marcaId)
    onSave(data)
  }

  return (
    <ModalShell title={row ? `Editar ${config.singular}` : config.novoLabel} onClose={onClose}>
      <form onSubmit={handleSubmit} className="space-y-4">
        {config.parent && (
          <Field label={config.parent.label}>
            <select
              className="input"
              value={marcaId}
              onChange={(e) => setMarcaId(e.target.value ? Number(e.target.value) : '')}
            >
              <option value="">Selecione...</option>
              {config.parent.options.map((o) => (
                <option key={o.id} value={o.id}>{o.nome}</option>
              ))}
            </select>
          </Field>
        )}
        <Field label="Nome">
          <input className="input" value={nome} onChange={(e) => setNome(e.target.value)} autoFocus />
        </Field>
        {config.hasDescricao && (
          <Field label="Descrição (opcional)">
            <input className="input" value={descricao} onChange={(e) => setDescricao(e.target.value)} />
          </Field>
        )}
        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" checked={ativo} onChange={(e) => setAtivo(e.target.checked)} />
          Ativo
        </label>

        {(localError || error) && (
          <p className="text-sm text-red-600">{localError || error}</p>
        )}

        <div className="flex justify-end gap-2 pt-2">
          <Button type="button" variant="secondary" onClick={onClose}>Cancelar</Button>
          <Button type="submit" isLoading={isSaving} className="bg-blue-600 hover:bg-blue-700">Salvar</Button>
        </div>
      </form>
    </ModalShell>
  )
}
