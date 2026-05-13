import { CheckCircle2, Clock, CreditCard, PackagePlus, Pause, Play, Send, XCircle } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { FinancialCard } from '../../components/FinancialCard.jsx'
import { FormField, inputClassName } from '../../components/FormField.jsx'
import { PriorityBadge } from '../../components/PriorityBadge.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { listCostCenters, listFinancialCategories } from '../../services/financialService.js'
import { listProducts } from '../../services/stockService.js'
import { addServiceOrderMaterial, addServiceOrderTime, getServiceOrder, runServiceOrderAction } from '../../services/serviceOrderService.js'
import { formatCurrency, formatDate } from '../../utils/formatters.js'

const materialColumns = [
  { key: 'produto_nome', label: 'Produto' },
  { key: 'quantidade', label: 'Qtd' },
  { key: 'custo_unitario', label: 'Custo unit.', render: (row) => formatCurrency(row.custo_unitario) },
  { key: 'custo_total', label: 'Total', render: (row) => formatCurrency(row.custo_total) },
]

const apontamentoColumns = [
  { key: 'colaborador_nome', label: 'Colaborador' },
  { key: 'data', label: 'Data', render: (row) => formatDate(row.data) },
  { key: 'hora_inicio', label: 'Inicio' },
  { key: 'hora_fim', label: 'Fim' },
  { key: 'total_horas', label: 'Horas' },
  { key: 'custo_total', label: 'Custo', render: (row) => formatCurrency(row.custo_total) },
]

export function ServiceOrderDetail() {
  const { id } = useParams()
  const [ordem, setOrdem] = useState(null)
  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [centers, setCenters] = useState([])
  const [material, setMaterial] = useState({ produto: '', quantidade: '1.0000', custo_unitario: '' })
  const [timeEntry, setTimeEntry] = useState({ colaborador: '', data: '', hora_inicio: '08:00', hora_fim: '09:00', tipo_hora: 'normal', custo_hora: '0.00' })
  const [billing, setBilling] = useState({ data_vencimento: '', categoria: '', centro_custo: '' })

  async function load() {
    setOrdem(await getServiceOrder(id))
  }

  useEffect(() => {
    load()
    Promise.all([listProducts(), listFinancialCategories(), listCostCenters()]).then(([productRows, categoryRows, centerRows]) => {
      setProducts(productRows)
      setCategories(categoryRows.filter((category) => category.tipo === 'receita'))
      setCenters(centerRows)
    })
  }, [id])

  async function run(action, payload = {}) {
    setOrdem(await runServiceOrderAction(id, action, payload))
  }

  async function submitMaterial(event) {
    event.preventDefault()
    await addServiceOrderMaterial(id, { ...material, produto: Number(material.produto), custo_unitario: material.custo_unitario || undefined })
    setMaterial({ produto: '', quantidade: '1.0000', custo_unitario: '' })
    await load()
  }

  async function submitTime(event) {
    event.preventDefault()
    await addServiceOrderTime(id, { ...timeEntry, colaborador: Number(timeEntry.colaborador || ordem.usuario_criador) })
    setTimeEntry({ colaborador: '', data: '', hora_inicio: '08:00', hora_fim: '09:00', tipo_hora: 'normal', custo_hora: '0.00' })
    await load()
  }

  if (!ordem) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando OS...</div>
  }

  const isFinal = ['finalizada', 'cancelada', 'faturada'].includes(ordem.status)
  const buttonClass = 'inline-flex items-center gap-2 rounded-md border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 disabled:cursor-not-allowed disabled:opacity-50'

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 xl:flex-row xl:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Ordens de Servico</p>
          <h2 className="text-2xl font-semibold text-slate-950">{ordem.numero} - {ordem.titulo}</h2>
          <div className="mt-2 flex flex-wrap gap-2">
            <StatusBadge status={ordem.status} />
            <PriorityBadge priority={ordem.prioridade} />
          </div>
        </div>
        <div className="flex flex-wrap gap-2">
          <button disabled={isFinal} onClick={() => run('enviar-aprovacao')} className={buttonClass}><Send className="h-4 w-4" />Aprovacao</button>
          <button disabled={isFinal} onClick={() => run('aprovar')} className={buttonClass}><CheckCircle2 className="h-4 w-4" />Aprovar</button>
          <button disabled={isFinal} onClick={() => run('iniciar')} className={buttonClass}><Play className="h-4 w-4" />Iniciar</button>
          <button disabled={isFinal} onClick={() => run('pausar')} className={buttonClass}><Pause className="h-4 w-4" />Pausar</button>
          <button disabled={isFinal} onClick={() => run('retomar')} className={buttonClass}><Play className="h-4 w-4" />Retomar</button>
          <button disabled={ordem.status === 'faturada'} onClick={() => run('finalizar')} className={buttonClass}><CheckCircle2 className="h-4 w-4" />Finalizar</button>
          <button disabled={ordem.status === 'faturada'} onClick={() => window.confirm('Cancelar esta OS?') && run('cancelar', { motivo: 'Cancelamento operacional solicitado.' })} className="inline-flex items-center gap-2 rounded-md border border-red-200 px-3 py-2 text-sm font-semibold text-red-700 disabled:opacity-50"><XCircle className="h-4 w-4" />Cancelar</button>
        </div>
      </div>
      <section className="grid gap-4 md:grid-cols-4">
        <FinancialCard label="Valor final" value={ordem.valor_final || ordem.valor_estimado} />
        <FinancialCard label="Custo materiais" value={ordem.custo_materiais} tone="amber" />
        <FinancialCard label="Custo mao de obra" value={ordem.custo_mao_obra} tone="amber" />
        <FinancialCard label="Custo total" value={ordem.custo_total} tone="red" />
      </section>
      <section className="grid gap-5 xl:grid-cols-2">
        <form onSubmit={submitMaterial} className="space-y-4 rounded-md border border-slate-200 bg-white p-5">
          <h3 className="inline-flex items-center gap-2 text-sm font-semibold uppercase text-slate-500"><PackagePlus className="h-4 w-4" />Materiais</h3>
          <div className="grid gap-3 md:grid-cols-3">
            <FormField label="Produto">
              <select className={inputClassName} value={material.produto} onChange={(event) => setMaterial((current) => ({ ...current, produto: event.target.value }))} required>
                <option value="">Selecione</option>
                {products.map((product) => <option key={product.id} value={product.id}>{product.nome}</option>)}
              </select>
            </FormField>
            <FormField label="Quantidade">
              <input className={inputClassName} value={material.quantidade} onChange={(event) => setMaterial((current) => ({ ...current, quantidade: event.target.value }))} required />
            </FormField>
            <FormField label="Custo unitario">
              <input className={inputClassName} value={material.custo_unitario} onChange={(event) => setMaterial((current) => ({ ...current, custo_unitario: event.target.value }))} placeholder="Custo medio" />
            </FormField>
          </div>
          <button disabled={isFinal} className="rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white disabled:opacity-50">Adicionar material</button>
          <DataTable columns={materialColumns} rows={ordem.materiais ?? []} loading={false} />
        </form>
        <form onSubmit={submitTime} className="space-y-4 rounded-md border border-slate-200 bg-white p-5">
          <h3 className="inline-flex items-center gap-2 text-sm font-semibold uppercase text-slate-500"><Clock className="h-4 w-4" />Apontamentos</h3>
          <div className="grid gap-3 md:grid-cols-3">
            <FormField label="Data">
              <input className={inputClassName} type="date" value={timeEntry.data} onChange={(event) => setTimeEntry((current) => ({ ...current, data: event.target.value }))} required />
            </FormField>
            <FormField label="Inicio">
              <input className={inputClassName} type="time" value={timeEntry.hora_inicio} onChange={(event) => setTimeEntry((current) => ({ ...current, hora_inicio: event.target.value }))} required />
            </FormField>
            <FormField label="Fim">
              <input className={inputClassName} type="time" value={timeEntry.hora_fim} onChange={(event) => setTimeEntry((current) => ({ ...current, hora_fim: event.target.value }))} required />
            </FormField>
            <FormField label="Tipo">
              <select className={inputClassName} value={timeEntry.tipo_hora} onChange={(event) => setTimeEntry((current) => ({ ...current, tipo_hora: event.target.value }))}>
                <option value="normal">Normal</option>
                <option value="extra_50">Extra 50%</option>
                <option value="extra_100">Extra 100%</option>
              </select>
            </FormField>
            <FormField label="Custo hora">
              <input className={inputClassName} value={timeEntry.custo_hora} onChange={(event) => setTimeEntry((current) => ({ ...current, custo_hora: event.target.value }))} />
            </FormField>
          </div>
          <button disabled={isFinal} className="rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white disabled:opacity-50">Adicionar apontamento</button>
          <DataTable columns={apontamentoColumns} rows={ordem.apontamentos ?? []} loading={false} />
        </form>
      </section>
      <form onSubmit={(event) => {
        event.preventDefault()
        const payload = Object.fromEntries(Object.entries(billing).filter(([, value]) => value))
        run('faturar', payload)
      }} className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-4">
        <h3 className="inline-flex items-center gap-2 text-sm font-semibold uppercase text-slate-500 md:col-span-4"><CreditCard className="h-4 w-4" />Faturamento</h3>
        <FormField label="Vencimento">
          <input className={inputClassName} type="date" value={billing.data_vencimento} onChange={(event) => setBilling((current) => ({ ...current, data_vencimento: event.target.value }))} />
        </FormField>
        <FormField label="Categoria">
          <select className={inputClassName} value={billing.categoria} onChange={(event) => setBilling((current) => ({ ...current, categoria: event.target.value }))}>
            <option value="">Usar cadastro da OS</option>
            {categories.map((category) => <option key={category.id} value={category.id}>{category.nome}</option>)}
          </select>
        </FormField>
        <FormField label="Centro de custo">
          <select className={inputClassName} value={billing.centro_custo} onChange={(event) => setBilling((current) => ({ ...current, centro_custo: event.target.value }))}>
            <option value="">Usar cadastro da OS</option>
            {centers.map((center) => <option key={center.id} value={center.id}>{center.codigo} - {center.nome}</option>)}
          </select>
        </FormField>
        <button disabled={ordem.status === 'faturada' || ordem.status === 'cancelada'} className="self-end rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white disabled:opacity-50">Faturar OS</button>
      </form>
      <section className="rounded-md border border-slate-200 bg-white p-5">
        <h3 className="text-sm font-semibold uppercase text-slate-500">Historico</h3>
        <div className="mt-4 space-y-3">
          {(ordem.historico ?? []).map((event) => (
            <div key={event.id} className="rounded-md border border-slate-100 p-3 text-sm">
              <p className="font-semibold text-slate-800">{event.tipo_evento}</p>
              <p className="text-slate-500">{event.descricao}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
