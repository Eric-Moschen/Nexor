import { FilePlus2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { listNFe } from '../../services/fiscalService.js'
import { formatCurrency, formatDate } from '../../utils/formatters.js'

const columns = [
  { key: 'numero', label: 'Numero', render: (row) => `${row.numero}/${row.serie}` },
  { key: 'tipo_operacao', label: 'Tipo' },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
  { key: 'valor_total', label: 'Total', render: (row) => formatCurrency(row.valor_total) },
  { key: 'data_emissao', label: 'Emissao', render: (row) => formatDate(row.data_emissao) },
  { key: 'id', label: 'Acoes', render: (row) => <Link className="font-semibold text-accent" to={`/fiscal/nfe/${row.id}`}>Detalhes</Link> },
]

export function NFeList() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listNFe().then(setRows).finally(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Fiscal</p>
          <h2 className="text-2xl font-semibold text-slate-950">Notas fiscais eletronicas</h2>
        </div>
        <Link to="/fiscal/nfe/nova" className="inline-flex items-center justify-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800">
          <FilePlus2 className="h-4 w-4" />
          Nova NF-e
        </Link>
      </div>
      <DataTable columns={columns} rows={rows} loading={loading} emptyMessage="Nenhuma NF-e encontrada." />
    </div>
  )
}
