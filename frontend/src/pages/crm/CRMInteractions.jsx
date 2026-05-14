import { CheckCircle2, Plus } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'

import { DataTable } from '../../components/DataTable.jsx'
import { FormField, inputClassName } from '../../components/FormField.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { createCrmInteraction, finalizeCrmInteraction, listCrmInteractions, listCustomers } from '../../services/relationshipService.js'
import { formatDate } from '../../utils/formatters.js'

export function CRMInteractions() {
  const [rows, setRows] = useState([])
  const [customers, setCustomers] = useState([])
  const [loading, setLoading] = useState(true)
  const [status, setStatus] = useState('')
  const [form, setForm] = useState({ cliente: '', tipo_interacao: 'ligacao', descricao: '', data: new Date().toISOString().slice(0, 16), status: 'aberto' })

  async function loadData() {
    const [interactionRows, customerRows] = await Promise.all([listCrmInteractions(), listCustomers()])
    setRows(interactionRows)
    setCustomers(customerRows)
    setLoading(false)
  }

  useEffect(() => {
    loadData()
  }, [])

  const columns = [
    { key: 'cliente_nome', label: 'Cliente' },
    { key: 'tipo_interacao', label: 'Tipo' },
    { key: 'descricao', label: 'Descricao' },
    { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
    { key: 'data', label: 'Data', render: (row) => formatDate(row.data) },
    {
      key: 'id',
      label: 'Acoes',
      render: (row) => row.status === 'finalizado' ? <span className="text-xs font-medium text-slate-400">Finalizada</span> : (
        <button type="button" onClick={() => handleFinalize(row.id)} className="inline-flex items-center gap-1 font-semibold text-emerald-700">
          <CheckCircle2 className="h-4 w-4" />
          Finalizar
        </button>
      ),
    },
  ]

  const filteredRows = useMemo(() => rows.filter((row) => !status || row.status === status), [rows, status])

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    await createCrmInteraction({ ...form, data: new Date(form.data).toISOString() })
    setForm((current) => ({ ...current, descricao: '' }))
    loadData()
  }

  async function handleFinalize(id) {
    await finalizeCrmInteraction(id)
    loadData()
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">CRM</p>
        <h2 className="text-2xl font-semibold text-slate-950">Interacoes operacionais</h2>
      </div>

      <form onSubmit={handleSubmit} className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 lg:grid-cols-[1fr_1fr_2fr_auto]">
        <FormField label="Cliente">
          <select className={inputClassName} value={form.cliente} onChange={(event) => updateField('cliente', event.target.value)} required>
            <option value="">Selecione</option>
            {customers.map((customer) => <option key={customer.id} value={customer.id}>{customer.razao_social}</option>)}
          </select>
        </FormField>
        <FormField label="Tipo">
          <select className={inputClassName} value={form.tipo_interacao} onChange={(event) => updateField('tipo_interacao', event.target.value)}>
            <option value="ligacao">Ligacao</option>
            <option value="whatsapp">WhatsApp</option>
            <option value="email">Email</option>
            <option value="visita">Visita</option>
            <option value="reuniao">Reuniao</option>
            <option value="suporte">Suporte</option>
            <option value="pos_venda">Pos-venda</option>
          </select>
        </FormField>
        <FormField label="Descricao">
          <input className={inputClassName} value={form.descricao} onChange={(event) => updateField('descricao', event.target.value)} required />
        </FormField>
        <button type="submit" className="mt-6 inline-flex h-10 items-center justify-center gap-2 rounded-md bg-midnight px-4 text-sm font-semibold text-white hover:bg-slate-800">
          <Plus className="h-4 w-4" />
          Registrar
        </button>
      </form>

      <section className="rounded-md border border-slate-200 bg-white p-4">
        <select className={`${inputClassName} max-w-xs`} value={status} onChange={(event) => setStatus(event.target.value)}>
          <option value="">Todos os status</option>
          <option value="aberto">Aberto</option>
          <option value="em_andamento">Em andamento</option>
          <option value="finalizado">Finalizado</option>
        </select>
      </section>

      <DataTable columns={columns} rows={filteredRows} loading={loading} emptyMessage="Nenhuma interacao CRM encontrada." />
    </div>
  )
}
