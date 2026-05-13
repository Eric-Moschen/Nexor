import { CheckCircle2, FileText, Send, ShieldCheck, XCircle } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { cancelNFe, getDanfeUrl, getNFe, getXmlUrl, sendNFe, signNFe, validateNFe } from '../../services/fiscalService.js'
import { formatCurrency, formatDate } from '../../utils/formatters.js'

const itemColumns = [
  { key: 'produto_nome', label: 'Produto' },
  { key: 'quantidade', label: 'Qtd' },
  { key: 'valor_unitario', label: 'Unitario', render: (row) => formatCurrency(row.valor_unitario) },
  { key: 'valor_total', label: 'Total', render: (row) => formatCurrency(row.valor_total) },
]

export function NFeDetail() {
  const { id } = useParams()
  const [nota, setNota] = useState(null)
  const [loading, setLoading] = useState(true)

  async function load() {
    setLoading(true)
    getNFe(id).then(setNota).finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
  }, [id])

  async function run(action) {
    const updated = await action(id)
    setNota(updated)
  }

  async function handleCancel() {
    if (!window.confirm('Confirmar cancelamento desta NF-e?')) return
    const updated = await cancelNFe(id, 'Cancelamento operacional solicitado pelo usuario fiscal.')
    setNota(updated)
  }

  if (loading || !nota) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando NF-e...</div>
  }

  const isFinal = ['autorizada', 'cancelada', 'denegada'].includes(nota.status)
  const buttonClass = 'inline-flex items-center gap-2 rounded-md border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 disabled:cursor-not-allowed disabled:opacity-50'

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Fiscal</p>
          <h2 className="text-2xl font-semibold text-slate-950">NF-e {nota.numero}/{nota.serie}</h2>
          <div className="mt-2 flex flex-wrap items-center gap-2 text-sm text-slate-500">
            <StatusBadge status={nota.status} />
            <span>{formatDate(nota.data_emissao)}</span>
            <span>{formatCurrency(nota.valor_total)}</span>
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <button disabled={isFinal} onClick={() => run(validateNFe)} className={buttonClass}><CheckCircle2 className="h-4 w-4" />Validar</button>
          <button disabled={isFinal} onClick={() => run(signNFe)} className={buttonClass}><ShieldCheck className="h-4 w-4" />Assinar</button>
          <button disabled={isFinal} onClick={() => run(sendNFe)} className="inline-flex items-center gap-2 rounded-md bg-midnight px-3 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"><Send className="h-4 w-4" />Enviar</button>
          <a href={getDanfeUrl(id)} className="inline-flex items-center gap-2 rounded-md border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700"><FileText className="h-4 w-4" />DANFE</a>
          <a href={getXmlUrl(id)} className="inline-flex items-center gap-2 rounded-md border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700"><FileText className="h-4 w-4" />XML</a>
          <button onClick={handleCancel} className="inline-flex items-center gap-2 rounded-md border border-red-200 px-3 py-2 text-sm font-semibold text-red-700"><XCircle className="h-4 w-4" />Cancelar</button>
        </div>
      </div>
      <DataTable columns={itemColumns} rows={nota.itens ?? []} loading={false} />
      <section className="rounded-md border border-slate-200 bg-white p-5">
        <h3 className="text-sm font-semibold uppercase text-slate-500">Eventos fiscais</h3>
        <div className="mt-4 space-y-3">
          {(nota.eventos ?? []).map((event) => (
            <div key={event.id} className="rounded-md border border-slate-100 p-3 text-sm">
              <p className="font-semibold text-slate-800">{event.tipo_evento}</p>
              <p className="text-slate-500">{event.mensagem}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
