import { Plus, Search } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { inputClassName } from '../../components/FormField.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { listCustomers } from '../../services/relationshipService.js'
import { formatCurrency, formatDate } from '../../utils/formatters.js'

const columns = [
  { key: 'razao_social', label: 'Cliente' },
  { key: 'documento', label: 'CPF/CNPJ' },
  { key: 'email', label: 'Email' },
  { key: 'telefone', label: 'Telefone' },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
  { key: 'limite_credito', label: 'Credito', render: (row) => formatCurrency(row.limite_credito ?? 0) },
  { key: 'created_at', label: 'Cadastro', render: (row) => formatDate(row.created_at) },
  { key: 'id', label: 'Acoes', render: (row) => <Link className="font-semibold text-accent" to={`/clientes/${row.id}`}>Detalhes</Link> },
]

export function CustomerList() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('')

  useEffect(() => {
    listCustomers().then(setRows).finally(() => setLoading(false))
  }, [])

  const filteredRows = useMemo(() => rows.filter((row) => {
    const term = query.toLowerCase()
    const matchesQuery = !term || [row.razao_social, row.nome_fantasia, row.documento, row.email].some((value) => String(value ?? '').toLowerCase().includes(term))
    return matchesQuery && (!status || row.status === status)
  }), [query, rows, status])

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Relacionamento</p>
          <h2 className="text-2xl font-semibold text-slate-950">Clientes</h2>
        </div>
        <Link to="/clientes/novo" className="inline-flex items-center justify-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800">
          <Plus className="h-4 w-4" />
          Novo cliente
        </Link>
      </div>

      <section className="grid gap-3 rounded-md border border-slate-200 bg-white p-4 md:grid-cols-[2fr_1fr]">
        <label className="relative">
          <Search className="pointer-events-none absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
          <input className={`${inputClassName} pl-9`} value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Buscar por nome, documento ou email" />
        </label>
        <select className={inputClassName} value={status} onChange={(event) => setStatus(event.target.value)}>
          <option value="">Todos os status</option>
          <option value="ativo">Ativo</option>
          <option value="inativo">Inativo</option>
          <option value="bloqueado">Bloqueado</option>
        </select>
      </section>

      <DataTable columns={columns} rows={filteredRows} loading={loading} emptyMessage="Nenhum cliente encontrado." />
    </div>
  )
}
