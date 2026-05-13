import { Plus } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { PriorityBadge } from '../../components/PriorityBadge.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { inputClassName } from '../../components/FormField.jsx'
import { listServiceOrders } from '../../services/serviceOrderService.js'
import { formatCurrency, formatDate } from '../../utils/formatters.js'

const columns = [
  { key: 'numero', label: 'Numero' },
  { key: 'cliente_nome', label: 'Cliente' },
  { key: 'titulo', label: 'Titulo' },
  { key: 'prioridade', label: 'Prioridade', render: (row) => <PriorityBadge priority={row.prioridade} /> },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
  { key: 'valor_final', label: 'Valor', render: (row) => formatCurrency(row.valor_final || row.valor_estimado) },
  { key: 'data_prevista', label: 'Prevista', render: (row) => formatDate(row.data_prevista) },
  { key: 'id', label: 'Acoes', render: (row) => <Link className="font-semibold text-accent" to={`/ordens-servico/${row.id}`}>Detalhes</Link> },
]

export function ServiceOrderList() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ status: '', prioridade: '' })

  useEffect(() => {
    listServiceOrders().then(setRows).finally(() => setLoading(false))
  }, [])

  const filteredRows = useMemo(() => rows.filter((row) => (!filters.status || row.status === filters.status) && (!filters.prioridade || row.prioridade === filters.prioridade)), [rows, filters])

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Ordens de Servico</p>
          <h2 className="text-2xl font-semibold text-slate-950">Controle operacional de OS</h2>
        </div>
        <Link to="/ordens-servico/nova" className="inline-flex items-center justify-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800">
          <Plus className="h-4 w-4" />
          Nova OS
        </Link>
      </div>
      <section className="grid gap-3 rounded-md border border-slate-200 bg-white p-4 md:grid-cols-4">
        <select className={inputClassName} value={filters.status} onChange={(event) => setFilters((current) => ({ ...current, status: event.target.value }))}>
          <option value="">Todos os status</option>
          <option value="rascunho">Rascunho</option>
          <option value="em_aprovacao">Em aprovacao</option>
          <option value="aprovada">Aprovada</option>
          <option value="em_execucao">Em execucao</option>
          <option value="finalizada">Finalizada</option>
          <option value="faturada">Faturada</option>
        </select>
        <select className={inputClassName} value={filters.prioridade} onChange={(event) => setFilters((current) => ({ ...current, prioridade: event.target.value }))}>
          <option value="">Todas as prioridades</option>
          <option value="baixa">Baixa</option>
          <option value="media">Media</option>
          <option value="alta">Alta</option>
          <option value="urgente">Urgente</option>
        </select>
      </section>
      <DataTable columns={columns} rows={filteredRows} loading={loading} emptyMessage="Nenhuma OS encontrada." />
    </div>
  )
}
