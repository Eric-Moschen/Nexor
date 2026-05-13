import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { FinancialCard } from '../../components/FinancialCard.jsx'
import { getFinancialDashboard } from '../../services/financialService.js'

export function FinancialDashboard() {
  const [dashboard, setDashboard] = useState(null)

  useEffect(() => {
    getFinancialDashboard().then(setDashboard)
  }, [])

  if (!dashboard) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando dashboard financeiro...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Financeiro</p>
          <h2 className="text-2xl font-semibold text-slate-950">Dashboard financeiro</h2>
        </div>
        <div className="flex gap-2">
          <Link className="rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white" to="/financeiro/cadastro/pagar">Nova conta a pagar</Link>
          <Link className="rounded-md border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700" to="/financeiro/cadastro/receber">Nova conta a receber</Link>
        </div>
      </div>
      <section className="grid gap-4 md:grid-cols-5">
        <FinancialCard label="Total a pagar" value={dashboard.total_a_pagar} tone="red" />
        <FinancialCard label="Total a receber" value={dashboard.total_a_receber} tone="green" />
        <FinancialCard label="Contas vencidas" value={dashboard.contas_vencidas} tone="amber" />
        <FinancialCard label="Recebiveis vencidos" value={dashboard.recebiveis_vencidos} tone="amber" />
        <FinancialCard label="Saldo projetado" value={dashboard.saldo_projetado} />
      </section>
    </div>
  )
}
