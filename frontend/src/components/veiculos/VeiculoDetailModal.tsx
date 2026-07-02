import { useState } from 'react'
import { FiEdit2, FiX, FiCalendar, FiShield, FiFileText } from 'react-icons/fi'
import { HiOutlineDatabase, HiOutlineTag, HiOutlineTruck, HiOutlineOfficeBuilding } from 'react-icons/hi'
import type { Veiculo } from '@/types'
import { Badge } from '@/components/ui/Badge'

type Props = {
  isOpen: boolean
  onClose: () => void
  veiculo: Veiculo | null
  loading: boolean
  tiposFrota: any[] | undefined
  onEdit: (veiculo: Veiculo) => void
}

const InfoRow = ({
  label,
  value,
  mono = false,
}: {
  label: string
  value: string | number | null | undefined
  mono?: boolean
}) => (
  <div className="flex justify-between items-baseline gap-4 py-2 border-b border-slate-100 dark:border-slate-800/50 last:border-0">
    <span className="text-xs text-slate-500 dark:text-slate-400 font-medium shrink-0">{label}</span>
    <span className={`text-sm text-slate-800 dark:text-slate-200 text-right truncate font-medium ${mono ? 'font-mono text-xs' : ''}`}>
      {value != null && value !== '' ? String(value) : <span className="text-slate-300 dark:text-slate-700">—</span>}
    </span>
  </div>
)

const fmtDate = (v: string | null | undefined) =>
  v ? new Date(v).toLocaleDateString('pt-BR') : null

export function VeiculoDetailModal({ isOpen, onClose, veiculo, loading, tiposFrota, onEdit }: Props) {
  const [activeTab, setActiveTab] = useState('ident')

  if (!isOpen) return null

  const isAtivo = veiculo?.situacao === 'ATIVO' || (veiculo?.situacao as string) === 'ATIVA'

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm transition-opacity duration-300">
      <div className="bg-white dark:bg-slate-900 rounded-2xl shadow-2xl w-full max-w-3xl max-h-[92vh] flex flex-col overflow-hidden border border-slate-100 dark:border-slate-800 transition-all duration-200">
        
        {/* Header com Gradiente Premium */}
        <div className="bg-gradient-to-r from-primary-600 to-indigo-700 dark:from-slate-900 dark:to-slate-850 px-8 py-5 text-white shrink-0 relative flex items-center justify-between border-b border-primary-700/20 dark:border-slate-800">
          {!loading && veiculo ? (
            <div className="flex items-center justify-between w-full">
              <div className="flex items-center gap-4">
                <div className="font-mono text-3xl font-extrabold tracking-wider bg-white/10 px-3 py-1 rounded-lg border border-white/20">
                  {veiculo.placa}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-primary-100 dark:text-slate-350">
                      {veiculo.marca?.nome} {veiculo.modelo?.nome}
                    </span>
                    <span className="text-sm text-primary-200/80 dark:text-slate-400">·</span>
                    <span className="text-sm text-primary-200/80 dark:text-slate-400 font-mono">
                      {veiculo.ano_fabricacao}
                    </span>
                  </div>
                  <div className="mt-1.5 flex items-center">
                    <Badge variant={isAtivo ? 'success' : 'danger'}>
                      {veiculo.situacao}
                    </Badge>
                  </div>
                </div>
              </div>
              <button
                onClick={onClose}
                className="text-white/80 hover:text-white bg-white/10 hover:bg-white/20 p-2 rounded-lg transition-all"
                aria-label="Fechar detalhes"
              >
                <FiX className="h-5 w-5" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3 text-primary-100 dark:text-slate-300 py-2">
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white" />
              <span className="text-sm font-medium">Carregando informações do veículo...</span>
            </div>
          )}
        </div>

        {/* Corpo do Modal */}
        <div className="flex-1 overflow-y-auto bg-slate-50 dark:bg-slate-950/60 p-6 scrollbar-none">
          {loading ? (
            <div className="flex flex-col items-center justify-center h-80 text-slate-400 dark:text-slate-600 gap-3">
              <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-primary-600" />
              <p className="text-sm font-medium">Carregando dados...</p>
            </div>
          ) : veiculo ? (
            <div className="space-y-6">
              {/* Grid Principal: Foto/Quick Stats (1 col) + Abas Detalhadas (2 cols) */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                
                {/* Coluna Esquerda: Foto & Stats Rápidos */}
                <div className="md:col-span-1 flex flex-col gap-4">
                  {/* Imagem Placeholder Premium */}
                  <div className="bg-gradient-to-br from-slate-100 to-slate-200 dark:from-slate-800 dark:to-slate-900 rounded-xl h-44 flex flex-col items-center justify-center border border-slate-200/50 dark:border-slate-800 shadow-sm relative overflow-hidden group">
                    <div className="absolute inset-0 bg-primary-600/5 dark:bg-primary-400/5 opacity-0 group-hover:opacity-100 transition-opacity duration-200" />
                    <HiOutlineTruck className="h-14 w-14 text-slate-400 dark:text-slate-500 mb-2 transition-transform duration-300 group-hover:scale-110" />
                    <p className="text-xs font-semibold text-slate-400 dark:text-slate-500 tracking-wider uppercase">Sem Foto Cadastrada</p>
                  </div>

                  {/* Quick Stats */}
                  <div className="grid grid-cols-2 gap-2">
                    {[
                      { label: 'PREFIXO', value: veiculo.prefixo || '—', icon: <HiOutlineTag className="text-primary-500 text-xs shrink-0" /> },
                      { label: 'COMBUSTÍVEL', value: veiculo.combustivel, icon: <HiOutlineDatabase className="text-orange-500 text-xs shrink-0" /> },
                      { label: 'TIPO REGISTRO', value: (veiculo.tipo_veiculo_nome ?? '—').replace(/_/g, ' ').slice(0, 15), icon: <HiOutlineTruck className="text-indigo-500 text-xs shrink-0" /> },
                      { label: 'CATEGORIA', value: veiculo.categoria?.nome?.slice(0, 12) || '—', icon: <HiOutlineOfficeBuilding className="text-emerald-500 text-xs shrink-0" /> },
                    ].map(({ label, value, icon }) => (
                      <div key={label} className="bg-white dark:bg-slate-900 rounded-xl p-3 border border-slate-100 dark:border-slate-800/80 shadow-sm flex flex-col justify-between">
                        <div className="flex items-center gap-1">
                          {icon}
                          <p className="text-slate-400 dark:text-slate-500 text-[10px] font-bold tracking-wider uppercase">{label}</p>
                        </div>
                        <p className="text-slate-800 dark:text-slate-200 font-extrabold text-sm mt-1.5 truncate">{value}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Coluna Direita: Abas & Informações */}
                <div className="md:col-span-2 flex flex-col">
                  {/* Tabs Modernas */}
                  <div className="flex gap-1 border-b border-slate-200 dark:border-slate-800 overflow-x-auto scrollbar-none pb-0.5">
                    {[
                      { id: 'ident', label: 'Identificação' },
                      { id: 'frota', label: 'Frota' },
                      { id: 'tecnico', label: 'Dados Técnicos' },
                      { id: 'admin', label: 'Administrativo' },
                    ].map((tab) => (
                      <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-2.5 text-xs font-semibold border-b-2 transition-all whitespace-nowrap -mb-[2px] ${
                          activeTab === tab.id
                            ? 'border-primary-500 text-primary-600 dark:text-primary-400 font-bold'
                            : 'border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200'
                        }`}
                      >
                        {tab.label}
                      </button>
                    ))}
                  </div>

                  {/* Tab Content Panel (Ajustado para evitar barras de rolagem desnecessárias) */}
                  <div className="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-100 dark:border-slate-800/80 shadow-sm mt-4 flex-1 flex flex-col justify-center min-h-[220px]">
                    <div className="space-y-1">
                      {activeTab === 'ident' && (
                        <>
                          <InfoRow label="RENAVAM" value={veiculo.renavam} mono />
                          <InfoRow label="Chassi" value={veiculo.chassi} mono />
                          <InfoRow label="Cor" value={veiculo.cor} />
                          <InfoRow label="Motorização" value={veiculo.motorizacao} />
                          <InfoRow label="UF" value={veiculo.uf} />
                          <InfoRow label="Município" value={veiculo.municipio} />
                        </>
                      )}

                      {activeTab === 'frota' && (
                        <>
                          <InfoRow label="Tipo de Frota" value={tiposFrota?.find(t => t.id === veiculo.tipo_frota_id)?.nome} />
                          <InfoRow label="Nº Patrimônio" value={veiculo.numero_patrimonio} />
                          <InfoRow label="Tipo Aquisição" value={veiculo.tipo_aquisicao} />
                          <InfoRow
                            label="Valor Aquisição"
                            value={veiculo.valor_aquisicao != null
                              ? `R$ ${veiculo.valor_aquisicao.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`
                              : null}
                          />
                          <InfoRow label="Locadora" value={veiculo.nome_locador} />
                          <InfoRow
                            label="Valor Locação"
                            value={veiculo.valor_locacao != null
                              ? `R$ ${veiculo.valor_locacao.toFixed(2)}/mês`
                              : null}
                          />
                        </>
                      )}

                      {activeTab === 'tecnico' && (
                        <>
                          <InfoRow label="Cilindrada" value={veiculo.cilindrada ? `${veiculo.cilindrada} cc` : null} />
                          <InfoRow label="Potência" value={veiculo.potencia ? `${veiculo.potencia} cv` : null} />
                          <InfoRow label="Transmissão" value={veiculo.transmissao} />
                          <InfoRow label="Tração" value={veiculo.tracao} />
                          <InfoRow label="Direção" value={veiculo.direcao} />
                          <InfoRow label="Vidros Elétricos" value={veiculo.vidros_eletricos != null ? (veiculo.vidros_eletricos ? 'Sim' : 'Não') : null} />
                          <InfoRow label="Ar Condicionado" value={veiculo.ar_condicionado != null ? (veiculo.ar_condicionado ? 'Sim' : 'Não') : null} />
                          {veiculo.pneu_dimensao && (
                            <InfoRow
                              label="Pneu"
                              value={[veiculo.pneu_dimensao, veiculo.pneu_velocidade, veiculo.pneu_carga].filter(Boolean).join(' · ')}
                            />
                          )}
                        </>
                      )}

                      {activeTab === 'admin' && (
                        <>
                          <InfoRow label="Unidade" value={veiculo.unidade?.nome} />
                          <InfoRow label="Subunidade" value={veiculo.subunidade?.nome} />
                          <InfoRow
                            label="Centro de Custo"
                            value={veiculo.centro_custo
                              ? `${veiculo.centro_custo.codigo} — ${veiculo.centro_custo.descricao}`
                              : null}
                          />
                          <InfoRow label="Tipo de Controle" value={veiculo.tipo_controle} />
                          <InfoRow label="Cap. Tanque" value={veiculo.capacidade_tanque ? `${veiculo.capacidade_tanque} L` : null} />
                          <InfoRow label="Cap. Passageiros" value={veiculo.capacidade_passageiros} />
                          <InfoRow label="Cap. Carga" value={veiculo.capacidade_carga ? `${veiculo.capacidade_carga} kg` : null} />
                        </>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Observações */}
              {veiculo.observacoes && (
                <div className="bg-white dark:bg-slate-900 rounded-xl p-5 border border-slate-100 dark:border-slate-800/80 shadow-sm transition-colors">
                  <div className="flex items-center gap-1.5 mb-2 border-b border-slate-100 dark:border-slate-800 pb-2">
                    <FiFileText className="text-slate-400 dark:text-slate-500 text-sm" />
                    <h4 className="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">Observações</h4>
                  </div>
                  <p className="text-sm text-slate-600 dark:text-slate-350 leading-relaxed font-medium">{veiculo.observacoes}</p>
                </div>
              )}

              {/* Documentação */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[
                  { label: 'Vencimento IPVA', value: fmtDate(veiculo.vencimento_ipva), icon: <FiCalendar className="text-orange-500" /> },
                  { label: 'Vencimento Licenciamento', value: fmtDate(veiculo.vencimento_licenciamento), icon: <FiFileText className="text-emerald-500" /> },
                  { label: 'Vencimento Seguro', value: fmtDate(veiculo.vencimento_seguro), icon: <FiShield className="text-indigo-500" /> },
                ].map(({ label, value, icon }) => (
                  <div key={label} className="bg-white dark:bg-slate-900 rounded-xl p-4 border border-slate-100 dark:border-slate-800/80 shadow-sm flex items-center gap-3">
                    <div className="p-2.5 rounded-lg bg-slate-50 dark:bg-slate-800/60 transition-colors">
                      {icon}
                    </div>
                    <div>
                      <p className="text-slate-400 dark:text-slate-500 text-[10px] font-bold tracking-wider uppercase">{label}</p>
                      <p className="text-slate-800 dark:text-slate-200 font-extrabold text-sm mt-0.5">{value || '—'}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ) : null}
        </div>

        {/* Rodapé Premium */}
        <div className="border-t border-slate-100 dark:border-slate-800 px-8 py-4 flex justify-end gap-3 bg-slate-50/60 dark:bg-slate-900/40 shrink-0 transition-colors duration-200">
          {!loading && veiculo && (
            <button
              onClick={() => onEdit(veiculo)}
              className="flex items-center gap-2 px-5 py-2.5 bg-primary-600 text-white rounded-xl hover:bg-primary-700 text-sm font-semibold transition-all shadow-md shadow-primary-500/10 active:scale-95"
            >
              <FiEdit2 size={14} />
              Editar Veículo
            </button>
          )}
          <button
            onClick={onClose}
            className="px-5 py-2.5 border border-slate-200 dark:border-slate-800 rounded-xl text-slate-700 dark:text-slate-350 hover:bg-slate-100 dark:hover:bg-slate-800 text-sm font-semibold transition-all active:scale-95"
          >
            Fechar
          </button>
        </div>
      </div>
    </div>
  )
}
