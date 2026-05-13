import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { Toast } from '../../components/Toast.jsx'
import { createProduct, listCategories, listUnits } from '../../services/stockService.js'

const initialForm = {
  codigo_interno: '',
  sku: '',
  codigo_barras: '',
  nome: '',
  descricao: '',
  categoria: '',
  unidade_medida: '',
  marca: '',
  custo_medio: '0.0000',
  preco_venda: '0.00',
  estoque_minimo: '0.0000',
}

export function ProductForm() {
  const navigate = useNavigate()
  const [form, setForm] = useState(initialForm)
  const [categories, setCategories] = useState([])
  const [units, setUnits] = useState([])
  const [saving, setSaving] = useState(false)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    Promise.all([listCategories(), listUnits()]).then(([categoryData, unitData]) => {
      setCategories(categoryData)
      setUnits(unitData)
    })
  }, [])

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    if (!form.codigo_interno || !form.sku || !form.nome || !form.categoria || !form.unidade_medida) {
      setToast({ message: 'Preencha codigo, SKU, nome, categoria e unidade.', tone: 'error' })
      return
    }
    setSaving(true)
    try {
      await createProduct(form)
      setToast({ message: 'Produto criado com sucesso.', tone: 'success' })
      setTimeout(() => navigate('/estoque'), 500)
    } catch {
      setToast({ message: 'Nao foi possivel criar o produto.', tone: 'error' })
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Estoque</p>
        <h2 className="text-2xl font-semibold text-slate-950">Cadastro de produto</h2>
      </div>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-3">
        <FormField label="Codigo interno">
          <input className={inputClassName} value={form.codigo_interno} onChange={(event) => updateField('codigo_interno', event.target.value)} />
        </FormField>
        <FormField label="SKU">
          <input className={inputClassName} value={form.sku} onChange={(event) => updateField('sku', event.target.value)} />
        </FormField>
        <FormField label="Codigo de barras">
          <input className={inputClassName} value={form.codigo_barras} onChange={(event) => updateField('codigo_barras', event.target.value)} />
        </FormField>
        <FormField label="Nome">
          <input className={inputClassName} value={form.nome} onChange={(event) => updateField('nome', event.target.value)} />
        </FormField>
        <FormField label="Categoria">
          <select className={inputClassName} value={form.categoria} onChange={(event) => updateField('categoria', event.target.value)}>
            <option value="">Selecione</option>
            {categories.map((category) => <option key={category.id} value={category.id}>{category.nome}</option>)}
          </select>
        </FormField>
        <FormField label="Unidade">
          <select className={inputClassName} value={form.unidade_medida} onChange={(event) => updateField('unidade_medida', event.target.value)}>
            <option value="">Selecione</option>
            {units.map((unit) => <option key={unit.id} value={unit.id}>{unit.sigla}</option>)}
          </select>
        </FormField>
        <FormField label="Marca">
          <input className={inputClassName} value={form.marca} onChange={(event) => updateField('marca', event.target.value)} />
        </FormField>
        <FormField label="Custo medio">
          <input className={inputClassName} type="number" min="0" step="0.0001" value={form.custo_medio} onChange={(event) => updateField('custo_medio', event.target.value)} />
        </FormField>
        <FormField label="Preco de venda">
          <input className={inputClassName} type="number" min="0" step="0.01" value={form.preco_venda} onChange={(event) => updateField('preco_venda', event.target.value)} />
        </FormField>
        <FormField label="Estoque minimo">
          <input className={inputClassName} type="number" min="0" step="0.0001" value={form.estoque_minimo} onChange={(event) => updateField('estoque_minimo', event.target.value)} />
        </FormField>
        <div className="md:col-span-3">
          <FormField label="Descricao">
            <textarea className={inputClassName} rows="4" value={form.descricao} onChange={(event) => updateField('descricao', event.target.value)} />
          </FormField>
        </div>
      </section>
      <div className="flex justify-end">
        <button className="rounded-md bg-midnight px-5 py-2 text-sm font-semibold text-white hover:bg-slate-800" disabled={saving}>
          {saving ? 'Salvando...' : 'Salvar produto'}
        </button>
      </div>
      <Toast message={toast?.message} tone={toast?.tone} onClose={() => setToast(null)} />
    </form>
  )
}
