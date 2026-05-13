import { Save } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { listCostCenters, listCustomers, listFinancialCategories } from '../../services/financialService.js'
import { createServiceOrder } from '../../services/serviceOrderService.js'

export function ServiceOrderForm() {
  const navigate = useNavigate()
  const [customers, setCustomers] = useState([])
  const [categories, setCategories] = useState([])
  const [centers, setCenters] = useState([])
  const [form, setForm] = useState({
    cliente: '',
    titulo: '',
    descricao_servico: '',
    tipo_servico: '',
    prioridade: 'media',
    data_prevista: '',
    valor_estimado: '0.00',
    categoria_financeira: '',
    centro_custo: '',
    itens: [{ descricao: '', quantidade: '1.0000', valor_unitario: '0.00' }],
  })

  useEffect(() => {
    Promise.all([listCustomers(), listFinancialCategories(), listCostCenters()]).then(([customerRows, categoryRows, centerRows]) => {
      setCustomers(customerRows)
      setCategories(categoryRows.filter((category) => category.tipo === 'receita'))
      setCenters(centerRows)
    })
  }, [])

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  function updateItem(field, value) {
    setForm((current) => ({ ...current, itens: [{ ...current.itens[0], [field]: value }] }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const payload = {
      ...form,
      cliente: Number(form.cliente),
      categoria_financeira: form.categoria_financeira ? Number(form.categoria_financeira) : null,
      centro_custo: form.centro_custo ? Number(form.centro_custo) : null,
      data_prevista: form.data_prevista || null,
      itens: form.itens[0].descricao ? form.itens : [],
    }
    const ordem = await createServiceOrder(payload)
    navigate(`/ordens-servico/${ordem.id}`)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Ordens de Servico</p>
        <h2 className="text-2xl font-semibold text-slate-950">Nova OS</h2>
      </div>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-3">
        <FormField label="Cliente">
          <select className={inputClassName} value={form.cliente} onChange={(event) => update('cliente', event.target.value)} required>
            <option value="">Selecione</option>
            {customers.map((customer) => <option key={customer.id} value={customer.id}>{customer.razao_social}</option>)}
          </select>
        </FormField>
        <FormField label="Titulo">
          <input className={inputClassName} value={form.titulo} onChange={(event) => update('titulo', event.target.value)} required />
        </FormField>
        <FormField label="Tipo de servico">
          <input className={inputClassName} value={form.tipo_servico} onChange={(event) => update('tipo_servico', event.target.value)} required />
        </FormField>
        <FormField label="Prioridade">
          <select className={inputClassName} value={form.prioridade} onChange={(event) => update('prioridade', event.target.value)}>
            <option value="baixa">Baixa</option>
            <option value="media">Media</option>
            <option value="alta">Alta</option>
            <option value="urgente">Urgente</option>
          </select>
        </FormField>
        <FormField label="Data prevista">
          <input className={inputClassName} type="date" value={form.data_prevista} onChange={(event) => update('data_prevista', event.target.value)} />
        </FormField>
        <FormField label="Valor estimado">
          <input className={inputClassName} value={form.valor_estimado} onChange={(event) => update('valor_estimado', event.target.value)} />
        </FormField>
        <FormField label="Categoria financeira">
          <select className={inputClassName} value={form.categoria_financeira} onChange={(event) => update('categoria_financeira', event.target.value)}>
            <option value="">Definir depois</option>
            {categories.map((category) => <option key={category.id} value={category.id}>{category.nome}</option>)}
          </select>
        </FormField>
        <FormField label="Centro de custo">
          <select className={inputClassName} value={form.centro_custo} onChange={(event) => update('centro_custo', event.target.value)}>
            <option value="">Definir depois</option>
            {centers.map((center) => <option key={center.id} value={center.id}>{center.codigo} - {center.nome}</option>)}
          </select>
        </FormField>
        <div className="md:col-span-3">
          <FormField label="Descricao do servico">
            <textarea className={inputClassName} value={form.descricao_servico} onChange={(event) => update('descricao_servico', event.target.value)} required />
          </FormField>
        </div>
      </section>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-3">
        <FormField label="Item de servico">
          <input className={inputClassName} value={form.itens[0].descricao} onChange={(event) => updateItem('descricao', event.target.value)} />
        </FormField>
        <FormField label="Quantidade">
          <input className={inputClassName} value={form.itens[0].quantidade} onChange={(event) => updateItem('quantidade', event.target.value)} />
        </FormField>
        <FormField label="Valor unitario">
          <input className={inputClassName} value={form.itens[0].valor_unitario} onChange={(event) => updateItem('valor_unitario', event.target.value)} />
        </FormField>
      </section>
      <button className="inline-flex items-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white">
        <Save className="h-4 w-4" />
        Salvar OS
      </button>
    </form>
  )
}
