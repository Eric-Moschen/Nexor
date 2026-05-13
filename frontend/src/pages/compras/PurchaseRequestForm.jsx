import { Plus, Trash2 } from 'lucide-react'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { Toast } from '../../components/Toast.jsx'
import { createPurchaseRequest } from '../../services/purchaseService.js'
import { listProducts, listUnits } from '../../services/stockService.js'

const emptyItem = { produto: '', descricao_livre: '', quantidade_solicitada: '1.0000', unidade_medida: '', observacao: '' }

export function PurchaseRequestForm() {
  const navigate = useNavigate()
  const [products, setProducts] = useState([])
  const [units, setUnits] = useState([])
  const [toast, setToast] = useState(null)
  const [form, setForm] = useState({
    centro_custo: '',
    justificativa: '',
    prioridade: 'media',
    observacoes: '',
    itens: [{ ...emptyItem }],
  })

  useEffect(() => {
    Promise.all([listProducts(), listUnits()]).then(([productData, unitData]) => {
      setProducts(productData)
      setUnits(unitData)
    })
  }, [])

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  function updateItem(index, field, value) {
    setForm((current) => ({
      ...current,
      itens: current.itens.map((item, itemIndex) => (itemIndex === index ? { ...item, [field]: value } : item)),
    }))
  }

  async function submit(event) {
    event.preventDefault()
    try {
      await createPurchaseRequest(form)
      setToast({ message: 'Solicitacao criada com sucesso.', tone: 'success' })
      setTimeout(() => navigate('/compras'), 500)
    } catch {
      setToast({ message: 'Nao foi possivel criar a solicitacao.', tone: 'error' })
    }
  }

  return (
    <form className="space-y-6" onSubmit={submit}>
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Compras</p>
        <h2 className="text-2xl font-semibold text-slate-950">Nova solicitacao</h2>
      </div>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-3">
        <FormField label="Centro de custo">
          <input className={inputClassName} value={form.centro_custo} onChange={(event) => updateField('centro_custo', event.target.value)} />
        </FormField>
        <FormField label="Prioridade">
          <select className={inputClassName} value={form.prioridade} onChange={(event) => updateField('prioridade', event.target.value)}>
            <option value="baixa">Baixa</option>
            <option value="media">Media</option>
            <option value="alta">Alta</option>
            <option value="urgente">Urgente</option>
          </select>
        </FormField>
        <FormField label="Observacoes">
          <input className={inputClassName} value={form.observacoes} onChange={(event) => updateField('observacoes', event.target.value)} />
        </FormField>
        <div className="md:col-span-3">
          <FormField label="Justificativa">
            <textarea className={inputClassName} rows="4" value={form.justificativa} onChange={(event) => updateField('justificativa', event.target.value)} />
          </FormField>
        </div>
      </section>
      <section className="space-y-4 rounded-md border border-slate-200 bg-white p-5 shadow-sm">
        <div className="flex items-center justify-between">
          <h3 className="text-base font-semibold text-slate-950">Itens</h3>
          <button type="button" className="inline-flex items-center gap-2 rounded-md border border-slate-200 px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50" onClick={() => updateField('itens', [...form.itens, { ...emptyItem }])}>
            <Plus className="h-4 w-4" />
            Adicionar
          </button>
        </div>
        {form.itens.map((item, index) => (
          <div key={index} className="grid gap-3 rounded-md border border-slate-100 p-3 md:grid-cols-5">
            <FormField label="Produto">
              <select className={inputClassName} value={item.produto} onChange={(event) => updateItem(index, 'produto', event.target.value)}>
                <option value="">Item nao cadastrado</option>
                {products.map((product) => <option key={product.id} value={product.id}>{product.nome}</option>)}
              </select>
            </FormField>
            <FormField label="Descricao livre">
              <input className={inputClassName} value={item.descricao_livre} onChange={(event) => updateItem(index, 'descricao_livre', event.target.value)} />
            </FormField>
            <FormField label="Quantidade">
              <input className={inputClassName} type="number" min="0.0001" step="0.0001" value={item.quantidade_solicitada} onChange={(event) => updateItem(index, 'quantidade_solicitada', event.target.value)} />
            </FormField>
            <FormField label="Unidade">
              <select className={inputClassName} value={item.unidade_medida} onChange={(event) => updateItem(index, 'unidade_medida', event.target.value)}>
                <option value="">Selecione</option>
                {units.map((unit) => <option key={unit.id} value={unit.id}>{unit.sigla}</option>)}
              </select>
            </FormField>
            <button type="button" className="mt-6 inline-flex h-10 items-center justify-center rounded-md border border-red-200 text-red-600 hover:bg-red-50" onClick={() => updateField('itens', form.itens.filter((_, itemIndex) => itemIndex !== index))}>
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        ))}
      </section>
      <div className="flex justify-end">
        <button className="rounded-md bg-midnight px-5 py-2 text-sm font-semibold text-white hover:bg-slate-800">Salvar solicitacao</button>
      </div>
      <Toast message={toast?.message} tone={toast?.tone} onClose={() => setToast(null)} />
    </form>
  )
}
