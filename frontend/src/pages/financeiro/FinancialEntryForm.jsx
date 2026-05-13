import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { Toast } from '../../components/Toast.jsx'
import {
  createPayable,
  createReceivable,
  listCostCenters,
  listCustomers,
  listFinancialCategories,
} from '../../services/financialService.js'
import { listSuppliers } from '../../services/purchaseService.js'

export function FinancialEntryForm() {
  const { type } = useParams()
  const navigate = useNavigate()
  const isPayable = type === 'pagar'
  const [categories, setCategories] = useState([])
  const [costCenters, setCostCenters] = useState([])
  const [suppliers, setSuppliers] = useState([])
  const [customers, setCustomers] = useState([])
  const [toast, setToast] = useState(null)
  const [form, setForm] = useState({
    fornecedor: '',
    cliente: '',
    descricao: '',
    categoria: '',
    centro_custo: '',
    valor_original: '',
    data_emissao: '',
    data_vencimento: '',
    tipo_pagamento: '',
    forma_recebimento: '',
    observacao: '',
  })

  useEffect(() => {
    Promise.all([listFinancialCategories(), listCostCenters(), listSuppliers(), listCustomers()]).then(([categoryData, costData, supplierData, customerData]) => {
      setCategories(categoryData)
      setCostCenters(costData)
      setSuppliers(supplierData)
      setCustomers(customerData)
    })
  }, [])

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function submit(event) {
    event.preventDefault()
    try {
      if (isPayable) {
        await createPayable({
          fornecedor: form.fornecedor,
          descricao: form.descricao,
          categoria: form.categoria,
          centro_custo: form.centro_custo,
          valor_original: form.valor_original,
          data_emissao: form.data_emissao,
          data_vencimento: form.data_vencimento,
          tipo_pagamento: form.tipo_pagamento,
          observacao: form.observacao,
        })
        navigate('/financeiro/contas-pagar')
      } else {
        await createReceivable({
          cliente: form.cliente,
          descricao: form.descricao,
          categoria: form.categoria,
          centro_custo: form.centro_custo,
          valor_original: form.valor_original,
          data_emissao: form.data_emissao,
          data_vencimento: form.data_vencimento,
          forma_recebimento: form.forma_recebimento,
          observacao: form.observacao,
        })
        navigate('/financeiro/contas-receber')
      }
    } catch {
      setToast({ message: 'Nao foi possivel salvar o lancamento financeiro.', tone: 'error' })
    }
  }

  const filteredCategories = categories.filter((category) => category.tipo === (isPayable ? 'despesa' : 'receita'))

  return (
    <form className="space-y-6" onSubmit={submit}>
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Financeiro</p>
        <h2 className="text-2xl font-semibold text-slate-950">{isPayable ? 'Nova conta a pagar' : 'Nova conta a receber'}</h2>
      </div>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-3">
        {isPayable ? (
          <FormField label="Fornecedor">
            <select className={inputClassName} value={form.fornecedor} onChange={(event) => updateField('fornecedor', event.target.value)}>
              <option value="">Selecione</option>
              {suppliers.map((supplier) => <option key={supplier.id} value={supplier.id}>{supplier.razao_social}</option>)}
            </select>
          </FormField>
        ) : (
          <FormField label="Cliente">
            <select className={inputClassName} value={form.cliente} onChange={(event) => updateField('cliente', event.target.value)}>
              <option value="">Selecione</option>
              {customers.map((customer) => <option key={customer.id} value={customer.id}>{customer.razao_social}</option>)}
            </select>
          </FormField>
        )}
        <FormField label="Categoria">
          <select className={inputClassName} value={form.categoria} onChange={(event) => updateField('categoria', event.target.value)}>
            <option value="">Selecione</option>
            {filteredCategories.map((category) => <option key={category.id} value={category.id}>{category.nome}</option>)}
          </select>
        </FormField>
        <FormField label="Centro de custo">
          <select className={inputClassName} value={form.centro_custo} onChange={(event) => updateField('centro_custo', event.target.value)}>
            <option value="">Selecione</option>
            {costCenters.map((center) => <option key={center.id} value={center.id}>{center.codigo} - {center.nome}</option>)}
          </select>
        </FormField>
        <FormField label="Descricao">
          <input className={inputClassName} value={form.descricao} onChange={(event) => updateField('descricao', event.target.value)} />
        </FormField>
        <FormField label="Valor">
          <input className={inputClassName} type="number" min="0.01" step="0.01" value={form.valor_original} onChange={(event) => updateField('valor_original', event.target.value)} />
        </FormField>
        <FormField label="Data emissao">
          <input className={inputClassName} type="date" value={form.data_emissao} onChange={(event) => updateField('data_emissao', event.target.value)} />
        </FormField>
        <FormField label="Data vencimento">
          <input className={inputClassName} type="date" value={form.data_vencimento} onChange={(event) => updateField('data_vencimento', event.target.value)} />
        </FormField>
        <FormField label={isPayable ? 'Tipo pagamento' : 'Forma recebimento'}>
          <input className={inputClassName} value={isPayable ? form.tipo_pagamento : form.forma_recebimento} onChange={(event) => updateField(isPayable ? 'tipo_pagamento' : 'forma_recebimento', event.target.value)} />
        </FormField>
        <FormField label="Observacao">
          <input className={inputClassName} value={form.observacao} onChange={(event) => updateField('observacao', event.target.value)} />
        </FormField>
      </section>
      <div className="flex justify-end">
        <button className="rounded-md bg-midnight px-5 py-2 text-sm font-semibold text-white hover:bg-slate-800">Salvar lancamento</button>
      </div>
      <Toast message={toast?.message} tone={toast?.tone} onClose={() => setToast(null)} />
    </form>
  )
}
