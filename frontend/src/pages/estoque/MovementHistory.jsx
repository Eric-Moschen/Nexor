import { useEffect, useState } from 'react'

import { DataTable } from '../../components/DataTable.jsx'
import { listMovements } from '../../services/stockService.js'
import { formatDate } from '../../utils/formatters.js'

const columns = [
  { key: 'data_movimentacao', label: 'Data', render: (row) => formatDate(row.data_movimentacao) },
  { key: 'produto_nome', label: 'Produto' },
  { key: 'tipo', label: 'Tipo' },
  { key: 'quantidade', label: 'Quantidade' },
  { key: 'saldo_anterior', label: 'Saldo anterior' },
  { key: 'saldo_posterior', label: 'Saldo posterior' },
  { key: 'usuario_responsavel_nome', label: 'Responsavel' },
]

export function MovementHistory() {
  const [movements, setMovements] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listMovements()
      .then(setMovements)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Estoque</p>
        <h2 className="text-2xl font-semibold text-slate-950">Historico de movimentacoes</h2>
      </div>
      <DataTable columns={columns} rows={movements} loading={loading} emptyMessage="Nenhuma movimentacao registrada." />
    </div>
  )
}
