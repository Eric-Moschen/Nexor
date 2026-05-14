import { Save } from 'lucide-react'
import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { createCustomer } from '../../services/relationshipService.js'

const initialState = {
  tipo_pessoa: 'juridica',
  razao_social: '',
  nome_fantasia: '',
  documento: '',
  inscricao_estadual: '',
  inscricao_municipal: '',
  email: '',
  telefone: '',
  whatsapp: '',
  limite_credito: '0.00',
  observacoes: '',
}

export function CustomerForm() {
  const [form, setForm] = useState(initialState)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setSaving(true)
    setError('')
    try {
      const cliente = await createCustomer(form)
      navigate(`/clientes/${cliente.id}`)
    } catch (requestError) {
      setError(requestError.response?.data?.message ?? 'Nao foi possivel salvar o cliente.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Clientes</p>
        <h2 className="text-2xl font-semibold text-slate-950">Novo cliente</h2>
      </div>
      {error ? <div className="rounded-md border border-red-200 bg-red-50 p-3 text-sm font-medium text-red-700">{error}</div> : null}
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-3">
        <FormField label="Tipo pessoa">
          <select className={inputClassName} value={form.tipo_pessoa} onChange={(event) => updateField('tipo_pessoa', event.target.value)}>
            <option value="juridica">Pessoa juridica</option>
            <option value="fisica">Pessoa fisica</option>
          </select>
        </FormField>
        <FormField label="Razao social">
          <input className={inputClassName} value={form.razao_social} onChange={(event) => updateField('razao_social', event.target.value)} required />
        </FormField>
        <FormField label="Nome fantasia">
          <input className={inputClassName} value={form.nome_fantasia} onChange={(event) => updateField('nome_fantasia', event.target.value)} />
        </FormField>
        <FormField label="CPF/CNPJ">
          <input className={inputClassName} value={form.documento} onChange={(event) => updateField('documento', event.target.value)} required />
        </FormField>
        <FormField label="Inscricao estadual">
          <input className={inputClassName} value={form.inscricao_estadual} onChange={(event) => updateField('inscricao_estadual', event.target.value)} />
        </FormField>
        <FormField label="Inscricao municipal">
          <input className={inputClassName} value={form.inscricao_municipal} onChange={(event) => updateField('inscricao_municipal', event.target.value)} />
        </FormField>
        <FormField label="Email">
          <input className={inputClassName} type="email" value={form.email} onChange={(event) => updateField('email', event.target.value)} />
        </FormField>
        <FormField label="Telefone">
          <input className={inputClassName} value={form.telefone} onChange={(event) => updateField('telefone', event.target.value)} />
        </FormField>
        <FormField label="WhatsApp">
          <input className={inputClassName} value={form.whatsapp} onChange={(event) => updateField('whatsapp', event.target.value)} />
        </FormField>
        <FormField label="Limite de credito">
          <input className={inputClassName} type="number" min="0" step="0.01" value={form.limite_credito} onChange={(event) => updateField('limite_credito', event.target.value)} />
        </FormField>
        <div className="md:col-span-2">
          <FormField label="Observacoes">
            <textarea className={inputClassName} rows="3" value={form.observacoes} onChange={(event) => updateField('observacoes', event.target.value)} />
          </FormField>
        </div>
      </section>
      <button type="submit" disabled={saving} className="inline-flex items-center justify-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 disabled:opacity-60">
        <Save className="h-4 w-4" />
        {saving ? 'Salvando...' : 'Salvar cliente'}
      </button>
    </form>
  )
}
