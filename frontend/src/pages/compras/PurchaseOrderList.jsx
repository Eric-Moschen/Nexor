import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { listPurchaseOrders } from '../../services/purchaseService.js'
import { formatDate } from '../../utils/formatters.js'

const columns = [
  { key: 'numero', label: 'Numero' },
  { key: 'fornecedor_nome', label: 'Fornecedor' },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
  { key: 'valor_total', label: 'Valor total' },
  { key: 'data_pedido', label: 'Data', render: (row) => formatDate(row.data_pedido) },
  { key: 'id', label: 'Acoes', render: (row) => <Link className="font-semibold text-accent" to={`/compras/pedidos/${row.id}`}>Detalhes</Link> },
]

export function PurchaseOrderList() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listPurchaseOrders().then(setRows).finally(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Compras</p>
        <h2 className="text-2xl font-semibold text-slate-950">Pedidos de compra</h2>
      </div>
      <DataTable columns={columns} rows={rows} loading={loading} emptyMessage="Nenhum pedido encontrado." />
    </div>
  )
}
