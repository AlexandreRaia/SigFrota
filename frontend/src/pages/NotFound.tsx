import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <div className="flex h-screen items-center justify-center text-center">
      <div>
        <p className="text-6xl font-bold text-gray-200">404</p>
        <h1 className="mt-2 text-2xl font-bold text-gray-900">Página não encontrada</h1>
        <p className="mt-2 text-gray-500">A página que você procura não existe.</p>
        <Link to="/dashboard" className="mt-4 inline-block text-primary-600 hover:underline">
          Voltar ao Dashboard
        </Link>
      </div>
    </div>
  )
}
