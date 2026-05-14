import { Plus, Search } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'
import { Link } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { inputClassName } from '../../components/FormField.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { listSuppliers } from '../../services/relationshipService.js'

const columns = [
  { key: 'razao_social', label: 'Fornecedor' },
  { key: 'documento', label: 'CPF/CNPJ' },
  { key: 'categoria', label: 'Categoria', render: (row) => <StatusBadge status={row.categoria} /> },
  { key: 'email', label: 'Email' },
  { key: 'telefone', label: 'Telefone' },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
]

export function SupplierList() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')
  const [category, setCategory] = useState('')

  useEffect(() => {
    listSuppliers().then(setRows).finally(() => setLoading(false))
  }, [])

  const filteredRows = useMemo(() => rows.filter((row) => {
    const term = query.toLowerCase()
    const matchesQuery = !term || [row.razao_social, row.nome_fantasia, row.documento, row.email].some((value) => String(value ?? '').toLowerCase().includes(term))
    return matchesQuery && (!category || row.categoria === category)
  }), [category, query, rows])

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Relacionamento</p>
          <h2 className="text-2xl font-semibold text-slate-950">Fornecedores</h2>
        </div>
        <Link to="/fornecedores/novo" className="inline-flex items-center justify-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800">
          <Plus className="h-4 w-4" />
          Novo fornecedor
        </Link>
      </div>
      <section className="grid gap-3 rounded-md border border-slate-200 bg-white p-4 md:grid-cols-[2fr_1fr]">
        <label className="relative">
          <Search className="pointer-events-none absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
          <input className={`${inputClassName} pl-9`} value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Buscar fornecedor" />
        </label>
        <select className={inputClassName} value={category} onChange={(event) => setCategory(event.target.value)}>
          <option value="">Todas as categorias</option>
          <option value="materia_prima">Materia-prima</option>
          <option value="ferramentas">Ferramentas</option>
          <option value="servicos">Servicos</option>
          <option value="transporte">Transporte</option>
          <option value="terceirizados">Terceirizados</option>
          <option value="outros">Outros</option>
        </select>
      </section>
      <DataTable columns={columns} rows={filteredRows} loading={loading} emptyMessage="Nenhum fornecedor encontrado." />
    </div>
  )
}
