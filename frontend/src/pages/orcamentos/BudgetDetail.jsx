import { CheckCircle2, FileText, Send, XCircle } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { FinancialCard } from '../../components/FinancialCard.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { getBudget, getBudgetPdfUrl, runBudgetAction } from '../../services/budgetService.js'
import { formatCurrency, formatDate } from '../../utils/formatters.js'

const productColumns = [
  { key: 'produto_nome', label: 'Produto' },
  { key: 'quantidade', label: 'Qtd' },
  { key: 'valor_unitario', label: 'Unitario', render: (row) => formatCurrency(row.valor_unitario) },
  { key: 'valor_total', label: 'Total', render: (row) => formatCurrency(row.valor_total) },
]

const serviceColumns = [
  { key: 'descricao', label: 'Servico' },
  { key: 'quantidade', label: 'Qtd' },
  { key: 'valor_unitario', label: 'Unitario', render: (row) => formatCurrency(row.valor_unitario) },
  { key: 'valor_total', label: 'Total', render: (row) => formatCurrency(row.valor_total) },
]

export function BudgetDetail() {
  const { id } = useParams()
  const [budget, setBudget] = useState(null)

  async function load() {
    setBudget(await getBudget(id))
  }

  useEffect(() => {
    load()
  }, [id])

  async function run(action, payload = {}) {
    setBudget(await runBudgetAction(id, action, payload))
  }

  if (!budget) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando orcamento...</div>
  }

  const locked = ['aprovado', 'convertido_os', 'cancelado'].includes(budget.status)
  const buttonClass = 'inline-flex items-center gap-2 rounded-md border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 disabled:cursor-not-allowed disabled:opacity-50'

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 lg:flex-row lg:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Orcamentos</p>
          <h2 className="text-2xl font-semibold text-slate-950">{budget.numero} - {budget.titulo}</h2>
          <div className="mt-2 flex flex-wrap items-center gap-2 text-sm text-slate-500">
            <StatusBadge status={budget.status} />
            <span>Validade {formatDate(budget.data_validade)}</span>
            {budget.ordem_servico ? <Link className="font-semibold text-accent" to={`/ordens-servico/${budget.ordem_servico}`}>OS vinculada</Link> : null}
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <button disabled={locked} onClick={() => run('enviar')} className={buttonClass}><Send className="h-4 w-4" />Enviar</button>
          <button disabled={budget.status === 'convertido_os' || budget.status === 'cancelado'} onClick={() => run('aprovar')} className={buttonClass}><CheckCircle2 className="h-4 w-4" />Aprovar</button>
          <button disabled={locked} onClick={() => run('reprovar', { motivo: 'Reprovado pelo cliente.' })} className={buttonClass}><XCircle className="h-4 w-4" />Reprovar</button>
          <button disabled={budget.status !== 'aprovado'} onClick={() => run('converter-os')} className="inline-flex items-center gap-2 rounded-md bg-midnight px-3 py-2 text-sm font-semibold text-white disabled:opacity-50"><CheckCircle2 className="h-4 w-4" />Converter OS</button>
          <a href={getBudgetPdfUrl(id)} className="inline-flex items-center gap-2 rounded-md border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700"><FileText className="h-4 w-4" />PDF</a>
        </div>
      </div>
      <section className="grid gap-4 md:grid-cols-5">
        <FinancialCard label="Produtos" value={budget.valor_produtos} />
        <FinancialCard label="Servicos" value={budget.valor_servicos} />
        <FinancialCard label="Desconto" value={budget.valor_desconto} tone="amber" />
        <FinancialCard label="Total" value={budget.valor_total} tone="green" />
        <FinancialCard label="Margem" value={`${budget.margem_estimada}%`} />
      </section>
      <DataTable columns={productColumns} rows={budget.itens_produto ?? []} loading={false} emptyMessage="Nenhum produto neste orcamento." />
      <DataTable columns={serviceColumns} rows={budget.itens_servico ?? []} loading={false} emptyMessage="Nenhum servico neste orcamento." />
      <section className="rounded-md border border-slate-200 bg-white p-5">
        <h3 className="text-sm font-semibold uppercase text-slate-500">Historico</h3>
        <div className="mt-4 space-y-3">
          {(budget.historico ?? []).map((event) => (
            <div key={event.id} className="rounded-md border border-slate-100 p-3 text-sm">
              <p className="font-semibold text-slate-800">{event.tipo_evento}</p>
              <p className="text-slate-500">{event.descricao}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
