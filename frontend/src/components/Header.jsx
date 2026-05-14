import { Bell, LogOut, Shield, UserCircle } from 'lucide-react'
import { Link } from 'react-router-dom'

import { useAuth } from '../hooks/useAuth.js'

export function Header() {
  const { user, logout } = useAuth()
  return (
    <header className="sticky top-0 z-10 flex h-16 items-center justify-between border-b border-slate-200 bg-white/95 px-4 backdrop-blur sm:px-6 lg:px-8">
      <div>
        <p className="text-sm font-medium text-slate-500">Ambiente corporativo</p>
        <h1 className="text-xl font-semibold text-slate-950">Base operacional Nexor</h1>
      </div>
      <div className="flex items-center gap-2">
        <Link to="/perfil" className="inline-flex items-center gap-2 rounded-md border border-slate-200 px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50">
          <UserCircle className="h-4 w-4" />
          {user?.first_name || user?.username || 'Usuario'}
        </Link>
        <button className="inline-flex h-10 w-10 items-center justify-center rounded-md border border-slate-200 text-slate-600 hover:bg-slate-50" title="Notificacoes">
          <Bell className="h-4 w-4" />
        </button>
        <button className="inline-flex h-10 w-10 items-center justify-center rounded-md bg-accent text-white hover:bg-violet-700" title="Seguranca">
          <Shield className="h-4 w-4" />
        </button>
        <button onClick={logout} className="inline-flex h-10 w-10 items-center justify-center rounded-md border border-slate-200 text-slate-600 hover:bg-slate-50" title="Sair">
          <LogOut className="h-4 w-4" />
        </button>
      </div>
    </header>
  )
}
