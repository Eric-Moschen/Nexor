import { useEffect, useState } from 'react'

import { DataTable } from '../../components/DataTable.jsx'
import { FormField, inputClassName } from '../../components/FormField.jsx'
import { createOperationNature, listOperationNatures } from '../../services/fiscalService.js'

const columns = [
  { key: 'codigo', label: 'Codigo' },
  { key: 'descricao', label: 'Descricao' },
  { key: 'tipo_operacao', label: 'Tipo' },
  { key: 'cfop_padrao', label: 'CFOP' },
]

export function OperationNatureList() {
  const [rows, setRows] = useState([])
  const [form, setForm] = useState({ codigo: '', descricao: '', tipo_operacao: 'venda', cfop_padrao: '5102', movimenta_estoque: true, gera_financeiro: true })

  async function load() {
    setRows(await listOperationNatures())
  }

  useEffect(() => {
    load()
  }, [])

  function update(field, value) {
    setForm((current) => ({ ...current, [field]: value }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    await createOperationNature(form)
    setForm({ codigo: '', descricao: '', tipo_operacao: 'venda', cfop_padrao: '5102', movimenta_estoque: true, gera_financeiro: true })
    await load()
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Fiscal</p>
        <h2 className="text-2xl font-semibold text-slate-950">Naturezas de operacao</h2>
      </div>
      <form onSubmit={handleSubmit} className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-5">
        <FormField label="Codigo">
          <input className={inputClassName} value={form.codigo} onChange={(event) => update('codigo', event.target.value)} required />
        </FormField>
        <FormField label="Descricao">
          <input className={inputClassName} value={form.descricao} onChange={(event) => update('descricao', event.target.value)} required />
        </FormField>
        <FormField label="Tipo">
          <select className={inputClassName} value={form.tipo_operacao} onChange={(event) => update('tipo_operacao', event.target.value)}>
            <option value="venda">Venda</option>
            <option value="compra">Compra</option>
            <option value="devolucao">Devolucao</option>
          </select>
        </FormField>
        <FormField label="CFOP">
          <input className={inputClassName} value={form.cfop_padrao} onChange={(event) => update('cfop_padrao', event.target.value)} required />
        </FormField>
        <button className="self-end rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white">Salvar</button>
      </form>
      <DataTable columns={columns} rows={rows} loading={false} />
    </div>
  )
}
