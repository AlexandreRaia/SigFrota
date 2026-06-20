import { NavLink } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { FaTachometerAlt, FaCar, FaUser, FaWrench, FaFileAlt } from 'react-icons/fa'

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: <FaTachometerAlt /> },
  { path: '/veiculos', label: 'Veículos', icon: <FaCar /> },
  { path: '/condutores', label: 'Condutores', icon: <FaUser /> },
  { path: '/manutencao', label: 'Manutenção', icon: <FaWrench /> },
  { path: '/multas', label: 'Multas', icon: <FaFileAlt /> },
]

type Props = {
  collapsed?: boolean
  mobileOpen?: boolean
  onCloseMobile?: () => void
}

export function Sidebar({ collapsed = false, mobileOpen = false, onCloseMobile }: Props) {
  const { user } = useAuth()

  return (
    <>
      {/* Overlay for mobile when menu is open */}
      <div
        className={`fixed inset-0 z-30 bg-black/40 transition-opacity md:hidden ${mobileOpen ? 'opacity-100 visible' : 'opacity-0 invisible'}`}
        onClick={onCloseMobile}
        aria-hidden={!mobileOpen}
      />

      <aside
        className={`fixed left-0 top-0 z-40 h-full flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 text-gray-800 dark:text-gray-100 transition-all duration-200 shadow-sm transform md:translate-x-0 md:static md:h-auto ${
          collapsed ? 'w-16' : 'w-64'
        } ${mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}
        aria-hidden={collapsed}
      >
      {/* Logo */}
      <div className="flex h-16 items-center px-4">
        <span className={`text-lg font-bold ${collapsed ? 'mx-auto' : ''}`}>
          {collapsed ? 'SF' : 'SigFrota'}
        </span>
      </div>

      {/* Nav */}
      <nav className="flex-1 space-y-1 px-2 py-4">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            onClick={() => onCloseMobile?.()}
            className={({ isActive }) =>
              `flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-primary-700 text-white'
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 dark:hover:bg-gray-800 dark:hover:text-white'
              }`
            }
            title={collapsed ? item.label : undefined}
            aria-label={item.label}
          >
            <span className="text-lg">{item.icon}</span>
            <span className={`sidebar-label ${collapsed ? 'max-w-0 opacity-0 scale-95' : 'max-w-[200px] opacity-100 scale-100'}`}>
              {!collapsed && item.label}
            </span>
          </NavLink>
        ))}
      </nav>

      {/* User info */}
      {user && (
        <div className="border-t border-gray-100 px-3 py-3">
          <p className="text-xs text-gray-500">Logado como</p>
          {!collapsed ? (
            <>
              <p className="text-sm font-medium text-gray-800 truncate">{user.username}</p>
              <span className="mt-1 inline-block rounded bg-primary-600 px-2 py-0.5 text-xs text-white">
                {user.perfil}
              </span>
            </>
          ) : (
            <div className="text-center text-xs text-gray-500">{user.username?.charAt(0)?.toUpperCase()}</div>
          )}
        </div>
      )}
    </aside>
    </>
  )
}
