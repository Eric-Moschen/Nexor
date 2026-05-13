import { Plus } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { listPurchaseRequests } from '../../services/purchaseService.js'
import { formatDate } from '../../utils/formatters.js'

const columns = [
  { key: 'numero', label: 'Numero' },
  { key: 'centro_custo', label: 'Centro de custo' },
  { key: 'prioridade', label: 'Prioridade' },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
  { key: 'data_solicitacao', label: 'Data', render: (row) => formatDate(row.data_solicitacao) },
  { key: 'id', label: 'Acoes', render: (row) => <Link className="font-semibold text-accent" to={`/compras/solicitacoes/${row.id}`}>Detalhes</Link> },
]

export function PurchaseRequestList() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listPurchaseRequests().then(setRows).finally(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Compras</p>
          <h2 className="text-2xl font-semibold text-slate-950">Solicitacoes de compra</h2>
        </div>
        <Link to="/compras/solicitacoes/nova" className="inline-flex items-center justify-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800">
          <Plus className="h-4 w-4" />
          Nova solicitacao
        </Link>
      </div>
      <DataTable columns={columns} rows={rows} loading={loading} emptyMessage="Nenhuma solicitacao encontrada." />
    </div>
  )
}
