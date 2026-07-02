import React, { useState } from 'react'
import { Edit2 } from 'lucide-react'

interface EditableFieldProps {
  label: string
  value: string | number | undefined
  field: string
  isEditMode: boolean
  onChange: (field: string, value: any) => void
  type?: 'text' | 'email' | 'number' | 'date' | 'select' | 'textarea'
  options?: { label: string; value: string | number }[]
  placeholder?: string
  icon?: React.ReactNode
}

export default function EditableField({
  label,
  value,
  field,
  isEditMode,
  onChange,
  type = 'text',
  options = [],
  placeholder = '',
  icon,
}: EditableFieldProps) {
  const [isHovering, setIsHovering] = useState(false)
  const [isLocalEdit, setIsLocalEdit] = useState(false)
  const [localValue, setLocalValue] = useState(String(value || ''))

  const handleInlineEdit = () => {
    setIsLocalEdit(true)
    setLocalValue(String(value || ''))
  }

  const handleInlineSave = () => {
    onChange(field, localValue)
    setIsLocalEdit(false)
  }

  const handleInlineCancel = () => {
    setIsLocalEdit(false)
  }

  if (isEditMode) {
    return (
      <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
          {icon && <span className="mr-2">{icon}</span>}
          {label}
        </label>
        {type === 'select' ? (
          <select
            value={value || ''}
            onChange={(e) => onChange(field, e.target.value)}
            className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
          >
            <option value="">{placeholder || 'Selecione...'}</option>
            {options.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        ) : type === 'textarea' ? (
          <textarea
            value={value || ''}
            onChange={(e) => onChange(field, e.target.value)}
            rows={4}
            className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder={placeholder}
          />
        ) : (
          <input
            type={type}
            value={value || ''}
            onChange={(e) => onChange(field, type === 'number' ? Number(e.target.value) : e.target.value)}
            className="w-full px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            placeholder={placeholder}
          />
        )}
      </div>
    )
  }

  if (isLocalEdit) {
    return (
      <div className="mb-4">
        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
          {icon && <span className="mr-2">{icon}</span>}
          {label}
        </label>
        <div className="flex gap-2">
          {type === 'select' ? (
            <select
              value={localValue}
              onChange={(e) => setLocalValue(e.target.value)}
              autoFocus
              className="flex-1 px-3 py-2 rounded-lg border-2 border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            >
              <option value="">{placeholder || 'Selecione...'}</option>
              {options.map((opt) => (
                <option key={opt.value} value={opt.value}>
                  {opt.label}
                </option>
              ))}
            </select>
          ) : (
            <input
              type={type}
              value={localValue}
              onChange={(e) => setLocalValue(e.target.value)}
              autoFocus
              className="flex-1 px-3 py-2 rounded-lg border-2 border-blue-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
            />
          )}
          <button
            onClick={handleInlineSave}
            className="px-3 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors font-medium"
          >
            ✓
          </button>
          <button
            onClick={handleInlineCancel}
            className="px-3 py-2 bg-gray-400 hover:bg-gray-500 text-white rounded-lg transition-colors font-medium"
          >
            ✕
          </button>
        </div>
      </div>
    )
  }

  return (
    <div
      className="mb-4 p-3 rounded-lg bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors group"
      onMouseEnter={() => setIsHovering(true)}
      onMouseLeave={() => setIsHovering(false)}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <label className="block text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wide mb-1">
            {icon && <span className="mr-2">{icon}</span>}
            {label}
          </label>
          <p className="text-lg font-medium text-gray-900 dark:text-white break-words">
            {value || '—'}
          </p>
        </div>
        {isHovering && (
          <button
            onClick={handleInlineEdit}
            className="ml-3 p-2 rounded-lg bg-blue-100 dark:bg-blue-900/30 hover:bg-blue-200 dark:hover:bg-blue-900/50 text-blue-600 dark:text-blue-400 opacity-0 group-hover:opacity-100 transition-all transform hover:scale-110"
            title="Editar"
          >
            <Edit2 size={16} />
          </button>
        )}
      </div>
    </div>
  )
}
