import { Plus } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { listReceivables } from '../../services/financialService.js'
import { formatDate } from '../../utils/formatters.js'

const columns = [
  { key: 'numero_lancamento', label: 'Lancamento' },
  { key: 'cliente_nome', label: 'Cliente' },
  { key: 'descricao', label: 'Descricao' },
  { key: 'valor_atual', label: 'Saldo' },
  { key: 'data_vencimento', label: 'Vencimento', render: (row) => formatDate(row.data_vencimento) },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
]

export function ReceivableList() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listReceivables().then(setRows).finally(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Financeiro</p>
          <h2 className="text-2xl font-semibold text-slate-950">Contas a receber</h2>
        </div>
        <Link to="/financeiro/cadastro/receber" className="inline-flex items-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white">
          <Plus className="h-4 w-4" />
          Nova conta
        </Link>
      </div>
      <DataTable columns={columns} rows={rows} loading={loading} emptyMessage="Nenhuma conta a receber encontrada." />
    </div>
  )
}
