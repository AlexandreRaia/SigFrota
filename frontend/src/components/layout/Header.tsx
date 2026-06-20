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
    <header className="flex h-16 items-center justify-between border-b border-gray-200 bg-white px-4 md:px-6">
      <div className="flex items-center gap-3">
        {/* Mobile menu button */}
        <button
          onClick={() => onMobileToggle?.()}
          aria-label="Abrir menu mobile"
          className="rounded-md p-2 text-gray-600 hover:bg-gray-100 md:hidden"
        >
          <HiOutlineMenu className="h-6 w-6" />
        </button>

        {/* Desktop collapse button */}
        <button
          onClick={onToggle}
          aria-label={collapsed ? 'Abrir menu' : 'Fechar menu'}
          className="hidden md:inline-flex rounded-md p-2 text-gray-600 hover:bg-gray-100"
        >
          <HiOutlineMenu className="h-6 w-6" />
        </button>
      </div>

      <div className="flex items-center gap-4">
        <span className="hidden sm:inline text-sm text-gray-600">
          {user?.first_name ? `Olá, ${user.first_name}` : user?.username}
        </span>
        <ThemeToggle />
        <button
          onClick={handleLogout}
          className="text-sm text-gray-500 hover:text-red-600 transition-colors"
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
      className="rounded-md p-2 text-gray-600 hover:bg-gray-100"
    >
      {theme === 'dark' ? <HiSun className="h-5 w-5" /> : <HiMoon className="h-5 w-5" />}
    </button>
  )
}
