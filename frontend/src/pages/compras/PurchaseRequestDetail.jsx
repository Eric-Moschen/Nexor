import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { FormField, inputClassName } from '../../components/FormField.jsx'
import { Modal } from '../../components/Modal.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { Toast } from '../../components/Toast.jsx'
import {
  approvePurchaseRequest,
  convertPurchaseRequestToOrder,
  getPurchaseRequest,
  listSuppliers,
  rejectPurchaseRequest,
  sendPurchaseRequestToApproval,
} from '../../services/purchaseService.js'

const itemColumns = [
  { key: 'produto_nome', label: 'Produto' },
  { key: 'descricao_livre', label: 'Descricao' },
  { key: 'quantidade_solicitada', label: 'Quantidade' },
  { key: 'unidade_medida_sigla', label: 'Unidade' },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
]

export function PurchaseRequestDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [request, setRequest] = useState(null)
  const [suppliers, setSuppliers] = useState([])
  const [toast, setToast] = useState(null)
  const [rejectOpen, setRejectOpen] = useState(false)
  const [convertOpen, setConvertOpen] = useState(false)
  const [motivo, setMotivo] = useState('')
  const [conversion, setConversion] = useState({ fornecedor: '', previsao_entrega: '', observacoes: '' })

  function load() {
    getPurchaseRequest(id).then(setRequest)
  }

  useEffect(() => {
    load()
    listSuppliers().then(setSuppliers)
  }, [id])

  async function runAction(action, successMessage) {
    try {
      await action()
      setToast({ message: successMessage, tone: 'success' })
      load()
    } catch {
      setToast({ message: 'Acao nao permitida para esta solicitacao.', tone: 'error' })
    }
  }

  if (!request) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando solicitacao...</div>
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-start">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Compras</p>
          <h2 className="text-2xl font-semibold text-slate-950">{request.numero}</h2>
          <div className="mt-2"><StatusBadge status={request.status} /></div>
        </div>
        <div className="flex flex-wrap gap-2">
          <button className="rounded-md border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50" onClick={() => runAction(() => sendPurchaseRequestToApproval(id), 'Solicitacao enviada para aprovacao.')}>Enviar aprovacao</button>
          <button className="rounded-md bg-emerald-600 px-3 py-2 text-sm font-semibold text-white hover:bg-emerald-700" onClick={() => runAction(() => approvePurchaseRequest(id), 'Solicitacao aprovada.')}>Aprovar</button>
          <button className="rounded-md bg-red-600 px-3 py-2 text-sm font-semibold text-white hover:bg-red-700" onClick={() => setRejectOpen(true)}>Reprovar</button>
          <button className="rounded-md bg-midnight px-3 py-2 text-sm font-semibold text-white hover:bg-slate-800" onClick={() => setConvertOpen(true)}>Converter pedido</button>
        </div>
      </div>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-3">
        <div>
          <p className="text-sm text-slate-500">Centro de custo</p>
          <p className="font-semibold text-slate-950">{request.centro_custo}</p>
        </div>
        <div>
          <p className="text-sm text-slate-500">Prioridade</p>
          <p className="font-semibold text-slate-950">{request.prioridade}</p>
        </div>
        <div>
          <p className="text-sm text-slate-500">Solicitante</p>
          <p className="font-semibold text-slate-950">{request.solicitante_nome}</p>
        </div>
        <div className="md:col-span-3">
          <p className="text-sm text-slate-500">Justificativa</p>
          <p className="text-slate-800">{request.justificativa}</p>
        </div>
      </section>
      <DataTable columns={itemColumns} rows={request.itens ?? []} loading={false} />
      <Modal open={rejectOpen} title="Reprovar solicitacao" onClose={() => setRejectOpen(false)}>
        <div className="space-y-4">
          <FormField label="Motivo">
            <textarea className={inputClassName} rows="4" value={motivo} onChange={(event) => setMotivo(event.target.value)} />
          </FormField>
          <button className="rounded-md bg-red-600 px-4 py-2 text-sm font-semibold text-white" onClick={() => runAction(() => rejectPurchaseRequest(id, motivo), 'Solicitacao reprovada.').then(() => setRejectOpen(false))}>Confirmar reprovacao</button>
        </div>
      </Modal>
      <Modal open={convertOpen} title="Converter em pedido" onClose={() => setConvertOpen(false)}>
        <div className="space-y-4">
          <FormField label="Fornecedor">
            <select className={inputClassName} value={conversion.fornecedor} onChange={(event) => setConversion({ ...conversion, fornecedor: event.target.value })}>
              <option value="">Selecione</option>
              {suppliers.map((supplier) => <option key={supplier.id} value={supplier.id}>{supplier.razao_social}</option>)}
            </select>
          </FormField>
          <FormField label="Previsao de entrega">
            <input className={inputClassName} type="date" value={conversion.previsao_entrega} onChange={(event) => setConversion({ ...conversion, previsao_entrega: event.target.value })} />
          </FormField>
          <button className="rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white" onClick={async () => {
            await convertPurchaseRequestToOrder(id, conversion)
            navigate('/compras/pedidos')
          }}>Criar pedido</button>
        </div>
      </Modal>
      <Toast message={toast?.message} tone={toast?.tone} onClose={() => setToast(null)} />
    </div>
  )
}
