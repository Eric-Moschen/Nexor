import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { Toast } from '../../components/Toast.jsx'
import { getPurchaseOrder, receivePurchaseOrderPartial, receivePurchaseOrderTotal } from '../../services/purchaseService.js'

export function PurchaseReceipt() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [order, setOrder] = useState(null)
  const [quantities, setQuantities] = useState({})
  const [toast, setToast] = useState(null)

  useEffect(() => {
    getPurchaseOrder(id).then(setOrder)
  }, [id])

  async function receivePartial() {
    const itens = Object.entries(quantities)
      .filter(([, quantidade]) => Number(quantidade) > 0)
      .map(([item, quantidade]) => ({ item: Number(item), quantidade }))
    try {
      await receivePurchaseOrderPartial(id, { itens, observacao: `Recebimento do pedido ${order.numero}` })
      navigate(`/compras/pedidos/${id}`)
    } catch {
      setToast({ message: 'Nao foi possivel registrar o recebimento.', tone: 'error' })
    }
  }

  async function receiveTotal() {
    await receivePurchaseOrderTotal(id, `Recebimento total do pedido ${order.numero}`)
    navigate(`/compras/pedidos/${id}`)
  }

  if (!order) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando pedido...</div>
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Compras</p>
        <h2 className="text-2xl font-semibold text-slate-950">Recebimento {order.numero}</h2>
      </div>
      <section className="space-y-3 rounded-md border border-slate-200 bg-white p-5 shadow-sm">
        {order.itens.map((item) => (
          <div key={item.id} className="grid gap-3 rounded-md border border-slate-100 p-3 md:grid-cols-4">
            <div>
              <p className="text-sm text-slate-500">Item</p>
              <p className="font-semibold text-slate-950">{item.descricao}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Comprado</p>
              <p className="font-semibold text-slate-950">{item.quantidade}</p>
            </div>
            <div>
              <p className="text-sm text-slate-500">Recebido</p>
              <p className="font-semibold text-slate-950">{item.quantidade_recebida}</p>
            </div>
            <FormField label="Receber agora">
              <input className={inputClassName} type="number" min="0" step="0.0001" value={quantities[item.id] ?? ''} onChange={(event) => setQuantities({ ...quantities, [item.id]: event.target.value })} />
            </FormField>
          </div>
        ))}
      </section>
      <div className="flex justify-end gap-2">
        <button className="rounded-md border border-slate-200 px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50" onClick={receivePartial}>Receber parcial</button>
        <button className="rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800" onClick={receiveTotal}>Receber total</button>
      </div>
      <Toast message={toast?.message} tone={toast?.tone} onClose={() => setToast(null)} />
    </div>
  )
}
