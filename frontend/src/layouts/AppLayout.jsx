import { Outlet } from 'react-router-dom'

import { Header } from '../components/Header.jsx'
import { Sidebar } from '../components/Sidebar.jsx'

export function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <div className="lg:pl-72">
        <Header />
        <main className="px-4 py-6 sm:px-6 lg:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
