import { Plus } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { inputClassName } from '../../components/FormField.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { listBudgets } from '../../services/budgetService.js'
import { formatCurrency, formatDate } from '../../utils/formatters.js'

const columns = [
  { key: 'numero', label: 'Numero' },
  { key: 'cliente_nome', label: 'Cliente' },
  { key: 'titulo', label: 'Titulo' },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
  { key: 'data_validade', label: 'Validade', render: (row) => formatDate(row.data_validade) },
  { key: 'valor_total', label: 'Total', render: (row) => formatCurrency(row.valor_total) },
  { key: 'margem_estimada', label: 'Margem', render: (row) => `${row.margem_estimada}%` },
  { key: 'id', label: 'Acoes', render: (row) => <Link className="font-semibold text-accent" to={`/orcamentos/${row.id}`}>Detalhes</Link> },
]

export function BudgetList() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [status, setStatus] = useState('')

  useEffect(() => {
    listBudgets().then(setRows).finally(() => setLoading(false))
  }, [])

  const filteredRows = useMemo(() => rows.filter((row) => !status || row.status === status), [rows, status])

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Orcamentos</p>
          <h2 className="text-2xl font-semibold text-slate-950">Propostas comerciais</h2>
        </div>
        <Link to="/orcamentos/novo" className="inline-flex items-center justify-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800">
          <Plus className="h-4 w-4" />
          Novo orcamento
        </Link>
      </div>
      <section className="grid gap-3 rounded-md border border-slate-200 bg-white p-4 md:grid-cols-4">
        <select className={inputClassName} value={status} onChange={(event) => setStatus(event.target.value)}>
          <option value="">Todos os status</option>
          <option value="rascunho">Rascunho</option>
          <option value="enviado">Enviado</option>
          <option value="aprovado">Aprovado</option>
          <option value="reprovado">Reprovado</option>
          <option value="convertido_os">Convertido em OS</option>
        </select>
      </section>
      <DataTable columns={columns} rows={filteredRows} loading={loading} emptyMessage="Nenhum orcamento encontrado." />
    </div>
  )
}
