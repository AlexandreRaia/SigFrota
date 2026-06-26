import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import { HiOutlineMenu, HiSun, HiMoon } from 'react-icons/hi'
import { useTheme } from '@/contexts/ThemeContext'

type Props = {
  collapsed: boolean
  onToggle: () => void
  onMobileToggle?: () => void
}

export function Header({ collapsed, onToggle, onMobileToggle }: Props) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header className="flex h-16 items-center justify-between border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 px-4 md:px-6 shrink-0">
      <div className="flex items-center gap-3">
        <button
          onClick={() => onMobileToggle?.()}
          aria-label="Abrir menu mobile"
          className="rounded-md p-2 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors md:hidden"
        >
          <HiOutlineMenu className="h-5 w-5" />
        </button>
        <button
          onClick={onToggle}
          aria-label={collapsed ? 'Abrir menu' : 'Fechar menu'}
          className="hidden md:inline-flex rounded-md p-2 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
        >
          <HiOutlineMenu className="h-5 w-5" />
        </button>
      </div>

      <div className="flex items-center gap-3">
        <span className="hidden sm:inline text-sm text-gray-600 dark:text-gray-300">
          {user?.first_name ? `Olá, ${user.first_name}` : user?.username}
        </span>
        <ThemeToggle />
        <button
          onClick={handleLogout}
          className="text-sm text-gray-500 dark:text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors px-2 py-1 rounded-md hover:bg-red-50 dark:hover:bg-red-900/20"
        >
          Sair
        </button>
      </div>
    </header>
  )
}

function ThemeToggle() {
  const { theme, toggle } = useTheme()
  return (
    <button
      onClick={toggle}
      aria-label="Alternar tema"
      className="rounded-md p-2 text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
      title={theme === 'dark' ? 'Mudar para claro' : 'Mudar para escuro'}
    >
      {theme === 'dark'
        ? <HiSun className="h-5 w-5 text-amber-400" />
        : <HiMoon className="h-5 w-5" />}
    </button>
  )
}
