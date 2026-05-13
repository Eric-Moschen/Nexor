import { useEffect, useState } from 'react'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { Toast } from '../../components/Toast.jsx'
import { listProducts, registerMovement } from '../../services/stockService.js'

export function StockMovement() {
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({ produto: '', tipo: 'entrada', quantidade: '', observacao: '' })
  const [saving, setSaving] = useState(false)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    listProducts().then(setProducts)
  }, [])

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    if (!form.produto || Number(form.quantidade) <= 0) {
      setToast({ message: 'Selecione um produto e informe quantidade maior que zero.', tone: 'error' })
      return
    }
    setSaving(true)
    try {
      await registerMovement(form.tipo, { produto: form.produto, quantidade: form.quantidade, observacao: form.observacao })
      setToast({ message: 'Movimentacao registrada com sucesso.', tone: 'success' })
      setForm({ produto: '', tipo: 'entrada', quantidade: '', observacao: '' })
    } catch {
      setToast({ message: 'Movimentacao rejeitada. Verifique saldo e dados informados.', tone: 'error' })
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="space-y-6" onSubmit={handleSubmit}>
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Estoque</p>
        <h2 className="text-2xl font-semibold text-slate-950">Movimentacao de estoque</h2>
      </div>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-2">
        <FormField label="Produto">
          <select className={inputClassName} value={form.produto} onChange={(event) => updateField('produto', event.target.value)}>
            <option value="">Selecione</option>
            {products.map((product) => <option key={product.id} value={product.id}>{product.codigo_interno} - {product.nome}</option>)}
          </select>
        </FormField>
        <FormField label="Tipo">
          <select className={inputClassName} value={form.tipo} onChange={(event) => updateField('tipo', event.target.value)}>
            <option value="entrada">Entrada</option>
            <option value="saida">Saida</option>
            <option value="ajuste">Ajuste</option>
          </select>
        </FormField>
        <FormField label="Quantidade">
          <input className={inputClassName} type="number" min="0.0001" step="0.0001" value={form.quantidade} onChange={(event) => updateField('quantidade', event.target.value)} />
        </FormField>
        <FormField label="Observacao">
          <input className={inputClassName} value={form.observacao} onChange={(event) => updateField('observacao', event.target.value)} />
        </FormField>
      </section>
      <div className="flex justify-end">
        <button className="rounded-md bg-midnight px-5 py-2 text-sm font-semibold text-white hover:bg-slate-800" disabled={saving}>
          {saving ? 'Registrando...' : 'Registrar movimentacao'}
        </button>
      </div>
      <Toast message={toast?.message} tone={toast?.tone} onClose={() => setToast(null)} />
    </form>
  )
}
