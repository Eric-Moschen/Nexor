import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { getPurchaseOrder } from '../../services/purchaseService.js'

const columns = [
  { key: 'descricao', label: 'Item' },
  { key: 'quantidade', label: 'Quantidade' },
  { key: 'quantidade_recebida', label: 'Recebido' },
  { key: 'valor_unitario', label: 'Valor unitario' },
  { key: 'valor_total', label: 'Valor total' },
]

export function PurchaseOrderDetail() {
  const { id } = useParams()
  const [order, setOrder] = useState(null)

  useEffect(() => {
    getPurchaseOrder(id).then(setOrder)
  }, [id])

  if (!order) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando pedido...</div>
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-start">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Compras</p>
          <h2 className="text-2xl font-semibold text-slate-950">{order.numero}</h2>
          <div className="mt-2"><StatusBadge status={order.status} /></div>
        </div>
        <Link className="rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800" to={`/compras/pedidos/${id}/recebimento`}>Registrar recebimento</Link>
      </div>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-3">
        <div>
          <p className="text-sm text-slate-500">Fornecedor</p>
          <p className="font-semibold text-slate-950">{order.fornecedor_nome}</p>
        </div>
        <div>
          <p className="text-sm text-slate-500">Valor total</p>
          <p className="font-semibold text-slate-950">{order.valor_total}</p>
        </div>
        <div>
          <p className="text-sm text-slate-500">Previsao</p>
          <p className="font-semibold text-slate-950">{order.previsao_entrega ?? '-'}</p>
        </div>
      </section>
      <DataTable columns={columns} rows={order.itens ?? []} loading={false} />
    </div>
  )
}
