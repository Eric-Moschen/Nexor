import { Save } from 'lucide-react'
import { useState } from 'react'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { createFiscalCompany } from '../../services/fiscalService.js'

export function FiscalCompanyConfig() {
  const [form, setForm] = useState({
    razao_social: '',
    nome_fantasia: '',
    cnpj: '',
    regime_tributario: 'simples_nacional',
    endereco_fiscal: '',
    municipio_ibge: '',
    uf: 'SP',
    cep: '',
    ambiente: 'homologacao',
    senha_certificado: '',
    certificado_a1: null,
  })
  const [saved, setSaved] = useState(false)

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    await createFiscalCompany(form)
    setSaved(true)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Fiscal</p>
        <h2 className="text-2xl font-semibold text-slate-950">Empresa fiscal</h2>
      </div>
      {saved ? <div className="rounded-md border border-emerald-200 bg-emerald-50 p-3 text-sm font-medium text-emerald-700">Empresa fiscal salva com sucesso.</div> : null}
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-3">
        {Object.entries({ razao_social: 'Razao social', nome_fantasia: 'Nome fantasia', cnpj: 'CNPJ', municipio_ibge: 'Municipio IBGE', uf: 'UF', cep: 'CEP', senha_certificado: 'Senha certificado' }).map(([field, label]) => (
          <FormField key={field} label={label}>
            <input className={inputClassName} type={field === 'senha_certificado' ? 'password' : 'text'} value={form[field]} onChange={(event) => update(field, event.target.value)} required={!['nome_fantasia', 'senha_certificado'].includes(field)} />
          </FormField>
        ))}
        <FormField label="Regime tributario">
          <select className={inputClassName} value={form.regime_tributario} onChange={(event) => update('regime_tributario', event.target.value)}>
            <option value="simples_nacional">Simples Nacional</option>
            <option value="lucro_presumido">Lucro Presumido</option>
            <option value="lucro_real">Lucro Real</option>
          </select>
        </FormField>
        <FormField label="Ambiente">
          <select className={inputClassName} value={form.ambiente} onChange={(event) => update('ambiente', event.target.value)}>
            <option value="homologacao">Homologacao</option>
            <option value="producao">Producao</option>
          </select>
        </FormField>
        <div className="md:col-span-3">
          <FormField label="Endereco fiscal">
            <textarea className={inputClassName} value={form.endereco_fiscal} onChange={(event) => update('endereco_fiscal', event.target.value)} required />
          </FormField>
        </div>
        <div className="md:col-span-3">
          <FormField label="Certificado A1">
            <input className={inputClassName} type="file" accept=".pfx,.p12" onChange={(event) => update('certificado_a1', event.target.files?.[0] ?? null)} />
          </FormField>
        </div>
      </section>
      <button className="inline-flex items-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white">
        <Save className="h-4 w-4" />
        Salvar empresa
      </button>
    </form>
  )
}
