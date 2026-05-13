import { useEffect, useState } from 'react'

import { FinancialCard } from '../../components/FinancialCard.jsx'
import { getCashFlow } from '../../services/financialService.js'

export function CashFlow() {
  const [flow, setFlow] = useState(null)

  useEffect(() => {
    getCashFlow().then(setFlow)
  }, [])

  if (!flow) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando fluxo de caixa...</div>
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Financeiro</p>
        <h2 className="text-2xl font-semibold text-slate-950">Fluxo de caixa</h2>
      </div>
      <section className="grid gap-4 md:grid-cols-3">
        <FinancialCard label="Total pago" value={flow.total_pago} tone="red" />
        <FinancialCard label="Total recebido" value={flow.total_recebido} tone="green" />
        <FinancialCard label="Saldo" value={flow.saldo} />
      </section>
    </div>
  )
}
