import { MessageSquarePlus } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { createCustomerInteraction, getCustomer, listCustomerHistory, listCustomerInteractions } from '../../services/relationshipService.js'
import { formatCurrency, formatDate } from '../../utils/formatters.js'

export function CustomerDetail() {
  const { id } = useParams()
  const [customer, setCustomer] = useState(null)
  const [history, setHistory] = useState([])
  const [interactions, setInteractions] = useState([])
  const [description, setDescription] = useState('')

  async function loadData() {
    const [detail, historyRows, interactionRows] = await Promise.all([getCustomer(id), listCustomerHistory(id), listCustomerInteractions(id)])
    setCustomer(detail)
    setHistory(historyRows)
    setInteractions(interactionRows)
  }

  useEffect(() => {
    loadData()
  }, [id])

  async function handleInteraction(event) {
    event.preventDefault()
    await createCustomerInteraction(id, {
      tipo_interacao: 'ligacao',
      descricao: description,
      data: new Date().toISOString(),
      status: 'aberto',
    })
    setDescription('')
    loadData()
  }

  if (!customer) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando cliente...</div>
  }

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-start">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Cliente</p>
          <h2 className="text-2xl font-semibold text-slate-950">{customer.razao_social}</h2>
          <p className="mt-1 text-sm text-slate-500">{customer.documento} | {customer.email || 'sem email'} | {customer.telefone || 'sem telefone'}</p>
        </div>
        <StatusBadge status={customer.status} />
      </div>

      <section className="grid gap-3 md:grid-cols-4">
        <InfoCard label="Tipo" value={customer.tipo_pessoa} />
        <InfoCard label="Credito" value={formatCurrency(customer.limite_credito ?? 0)} />
        <InfoCard label="Contatos" value={customer.contatos?.length ?? 0} />
        <InfoCard label="Cadastro" value={formatDate(customer.created_at)} />
      </section>

      <section className="grid gap-5 lg:grid-cols-[1fr_1fr]">
        <div className="rounded-md border border-slate-200 bg-white p-5">
          <h3 className="text-base font-semibold text-slate-950">Interacoes</h3>
          <form onSubmit={handleInteraction} className="mt-4 space-y-3">
            <FormField label="Nova interacao">
              <textarea className={inputClassName} rows="3" value={description} onChange={(event) => setDescription(event.target.value)} required />
            </FormField>
            <button type="submit" className="inline-flex items-center gap-2 rounded-md bg-midnight px-3 py-2 text-sm font-semibold text-white hover:bg-slate-800">
              <MessageSquarePlus className="h-4 w-4" />
              Registrar
            </button>
          </form>
          <div className="mt-5 space-y-3">
            {interactions.map((item) => (
              <div key={item.id} className="rounded-md border border-slate-100 bg-slate-50 p-3">
                <div className="flex items-center justify-between gap-2">
                  <span className="text-sm font-semibold text-slate-800">{item.tipo_interacao}</span>
                  <StatusBadge status={item.status} />
                </div>
                <p className="mt-2 text-sm text-slate-600">{item.descricao}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-md border border-slate-200 bg-white p-5">
          <h3 className="text-base font-semibold text-slate-950">Historico</h3>
          <div className="mt-4 space-y-3">
            {history.map((item) => (
              <div key={item.id} className="border-l-2 border-accent pl-3">
                <p className="text-sm font-semibold text-slate-800">{item.tipo_evento}</p>
                <p className="text-sm text-slate-600">{item.descricao}</p>
                <p className="mt-1 text-xs text-slate-400">{formatDate(item.created_at)}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}

function InfoCard({ label, value }) {
  return (
    <div className="rounded-md border border-slate-200 bg-white p-4">
      <p className="text-xs font-semibold uppercase text-slate-500">{label}</p>
      <p className="mt-2 text-lg font-semibold text-slate-950">{value}</p>
    </div>
  )
}
