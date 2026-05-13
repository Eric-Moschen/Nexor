import { Save } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { listCustomers } from '../../services/financialService.js'
import { listProducts } from '../../services/stockService.js'
import { createBudget } from '../../services/budgetService.js'

export function BudgetForm() {
  const navigate = useNavigate()
  const [customers, setCustomers] = useState([])
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({
    cliente: '',
    titulo: '',
    descricao: '',
    data_validade: '',
    condicao_pagamento: '',
    prazo_entrega: '',
    valor_desconto: '0.00',
    itens_produto: [{ produto: '', quantidade: '1.0000', valor_unitario: '0.00', desconto: '0.00' }],
    itens_servico: [{ descricao: '', quantidade: '1.0000', custo_estimado: '0.00', valor_unitario: '0.00', desconto: '0.00' }],
  })

  useEffect(() => {
    Promise.all([listCustomers(), listProducts()]).then(([customerRows, productRows]) => {
      setCustomers(customerRows)
      setProducts(productRows)
    })
  }, [])

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  function updateProduct(field, value) {
    setForm((current) => ({ ...current, itens_produto: [{ ...current.itens_produto[0], [field]: value }] }))
  }

  function updateService(field, value) {
    setForm((current) => ({ ...current, itens_servico: [{ ...current.itens_servico[0], [field]: value }] }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    const payload = {
      ...form,
      cliente: Number(form.cliente),
      itens_produto: form.itens_produto[0].produto ? [{ ...form.itens_produto[0], produto: Number(form.itens_produto[0].produto) }] : [],
      itens_servico: form.itens_servico[0].descricao ? form.itens_servico : [],
    }
    const budget = await createBudget(payload)
    navigate(`/orcamentos/${budget.id}`)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Orcamentos</p>
        <h2 className="text-2xl font-semibold text-slate-950">Novo orcamento</h2>
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
        <FormField label="Validade">
          <input className={inputClassName} type="date" value={form.data_validade} onChange={(event) => update('data_validade', event.target.value)} required />
        </FormField>
        <FormField label="Condicao de pagamento">
          <input className={inputClassName} value={form.condicao_pagamento} onChange={(event) => update('condicao_pagamento', event.target.value)} />
        </FormField>
        <FormField label="Prazo de entrega">
          <input className={inputClassName} value={form.prazo_entrega} onChange={(event) => update('prazo_entrega', event.target.value)} />
        </FormField>
        <FormField label="Desconto geral">
          <input className={inputClassName} value={form.valor_desconto} onChange={(event) => update('valor_desconto', event.target.value)} />
        </FormField>
        <div className="md:col-span-3">
          <FormField label="Descricao">
            <textarea className={inputClassName} value={form.descricao} onChange={(event) => update('descricao', event.target.value)} />
          </FormField>
        </div>
      </section>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-4">
        <h3 className="text-sm font-semibold uppercase text-slate-500 md:col-span-4">Item de produto</h3>
        <FormField label="Produto">
          <select className={inputClassName} value={form.itens_produto[0].produto} onChange={(event) => updateProduct('produto', event.target.value)}>
            <option value="">Sem produto</option>
            {products.map((product) => <option key={product.id} value={product.id}>{product.nome}</option>)}
          </select>
        </FormField>
        <FormField label="Quantidade">
          <input className={inputClassName} value={form.itens_produto[0].quantidade} onChange={(event) => updateProduct('quantidade', event.target.value)} />
        </FormField>
        <FormField label="Valor unitario">
          <input className={inputClassName} value={form.itens_produto[0].valor_unitario} onChange={(event) => updateProduct('valor_unitario', event.target.value)} />
        </FormField>
        <FormField label="Desconto item">
          <input className={inputClassName} value={form.itens_produto[0].desconto} onChange={(event) => updateProduct('desconto', event.target.value)} />
        </FormField>
      </section>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-4">
        <h3 className="text-sm font-semibold uppercase text-slate-500 md:col-span-4">Item de servico</h3>
        <FormField label="Servico">
          <input className={inputClassName} value={form.itens_servico[0].descricao} onChange={(event) => updateService('descricao', event.target.value)} />
        </FormField>
        <FormField label="Quantidade">
          <input className={inputClassName} value={form.itens_servico[0].quantidade} onChange={(event) => updateService('quantidade', event.target.value)} />
        </FormField>
        <FormField label="Custo estimado">
          <input className={inputClassName} value={form.itens_servico[0].custo_estimado} onChange={(event) => updateService('custo_estimado', event.target.value)} />
        </FormField>
        <FormField label="Valor unitario">
          <input className={inputClassName} value={form.itens_servico[0].valor_unitario} onChange={(event) => updateService('valor_unitario', event.target.value)} />
        </FormField>
      </section>
      <button className="inline-flex items-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white">
        <Save className="h-4 w-4" />
        Salvar orcamento
      </button>
    </form>
  )
}
