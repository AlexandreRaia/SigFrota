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
      {/* Mobile overlay */}
      <div
        className={`fixed inset-0 z-30 bg-black/50 transition-opacity md:hidden ${mobileOpen ? 'opacity-100 visible' : 'opacity-0 invisible'}`}
        onClick={onCloseMobile}
        aria-hidden={!mobileOpen}
      />

      <aside
        className={`fixed left-0 top-0 z-40 h-full flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700/50 transition-all duration-200 shadow-sm md:shadow-none md:static md:h-auto transform md:translate-x-0 ${
          collapsed ? 'w-16' : 'w-64'
        } ${mobileOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}`}
      >
        {/* Logo */}
        <div className={`flex h-16 items-center border-b border-gray-100 dark:border-gray-700/50 px-4 shrink-0 ${collapsed ? 'justify-center' : 'gap-2'}`}>
          <div className="flex items-center justify-center w-8 h-8 bg-blue-600 rounded-lg shrink-0">
            <span className="text-white text-sm font-bold">SF</span>
          </div>
          {!collapsed && (
            <div>
              <span className="text-base font-bold text-gray-900 dark:text-white">SigFrota</span>
              <p className="text-xs text-gray-400 dark:text-gray-500 leading-none">Gestão de Frota</p>
            </div>
          )}
        </div>

        {/* Nav */}
        <nav className="flex-1 space-y-0.5 px-2 py-4 overflow-y-auto">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              onClick={() => onCloseMobile?.()}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'
                }`
              }
              title={collapsed ? item.label : undefined}
            >
              <span className="text-base shrink-0">{item.icon}</span>
              {!collapsed && <span>{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        {/* User info */}
        {user && (
          <div className={`border-t border-gray-100 dark:border-gray-700/50 px-3 py-3 shrink-0 ${collapsed ? 'text-center' : ''}`}>
            {collapsed ? (
              <div className="w-8 h-8 mx-auto rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
                <span className="text-xs font-bold text-blue-600 dark:text-blue-400">
                  {user.username?.charAt(0)?.toUpperCase()}
                </span>
              </div>
            ) : (
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center shrink-0">
                  <span className="text-xs font-bold text-blue-600 dark:text-blue-400">
                    {user.username?.charAt(0)?.toUpperCase()}
                  </span>
                </div>
                <div className="min-w-0">
                  <p className="text-sm font-medium text-gray-800 dark:text-gray-200 truncate">{user.username}</p>
                  <span className="text-xs text-gray-500 dark:text-gray-400">{user.perfil}</span>
                </div>
              </div>
            )}
          </div>
        )}
      </aside>
    </>
  )
}
