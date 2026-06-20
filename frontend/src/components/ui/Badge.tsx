type BadgeVariant = 'default' | 'success' | 'warning' | 'danger' | 'info'

const variantClasses: Record<BadgeVariant, string> = {
  default: 'bg-gray-100 text-gray-800',
  success: 'bg-green-100 text-green-800',
  warning: 'bg-yellow-100 text-yellow-800',
  danger: 'bg-red-100 text-red-800',
  info: 'bg-blue-100 text-blue-800',
}

interface BadgeProps {
  children: React.ReactNode
  variant?: BadgeVariant
  className?: string
}

import React from 'react'

export function Badge({ children, variant = 'default', className = '' }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${variantClasses[variant]} ${className}`}
    >
      {children}
    </span>
  )
}

// ── Helpers para status específicos ───────────────────────────────────────────

export function StatusVeiculoBadge({ status }: { status: string }) {
  const map: Record<string, BadgeVariant> = {
    DISPONIVEL: 'success',
    EM_MANUTENCAO: 'warning',
    INATIVO: 'danger',
  }
  const labels: Record<string, string> = {
    DISPONIVEL: 'Disponível',
    EM_MANUTENCAO: 'Em Manutenção',
    INATIVO: 'Inativo',
  }
  return <Badge variant={map[status] ?? 'default'}>{labels[status] ?? status}</Badge>
}

export function StatusMultaBadge({ status }: { status: string }) {
  const map: Record<string, BadgeVariant> = {
    PENDENTE: 'warning',
    PAGA: 'success',
    CONTESTADA: 'info',
    VENCIDA: 'danger',
  }
  return <Badge variant={map[status] ?? 'default'}>{status}</Badge>
}

export function EtapaSMVBadge({ etapa }: { etapa: string }) {
  const map: Record<string, BadgeVariant> = {
    SOLICITACAO: 'default',
    RECEPCAO: 'info',
    DIAGNOSTICO: 'info',
    ORCAMENTO: 'warning',
    APROVACAO: 'warning',
    EXECUCAO: 'warning',
    RETIRADA: 'info',
    EMISSAO_NF: 'info',
    FINALIZADO: 'success',
  }
  return <Badge variant={map[etapa] ?? 'default'}>{etapa}</Badge>
}
