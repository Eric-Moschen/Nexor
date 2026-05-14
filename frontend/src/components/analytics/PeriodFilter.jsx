import { inputClassName } from '../FormField.jsx'

export function PeriodFilter({ filters, onChange }) {
  function update(field, value) {
    onChange({ ...filters, [field]: value })
  }

  return (
    <section className="grid gap-3 rounded-md border border-slate-200 bg-white p-4 md:grid-cols-4">
      <input className={inputClassName} type="date" value={filters.data_inicial ?? ''} onChange={(event) => update('data_inicial', event.target.value)} />
      <input className={inputClassName} type="date" value={filters.data_final ?? ''} onChange={(event) => update('data_final', event.target.value)} />
      <select className={inputClassName} value={filters.status ?? ''} onChange={(event) => update('status', event.target.value)}>
        <option value="">Todos os status</option>
        <option value="pendente">Pendente</option>
        <option value="pago">Pago</option>
        <option value="recebido">Recebido</option>
        <option value="vencido">Vencido</option>
      </select>
      <button type="button" onClick={() => onChange({})} className="rounded-md border border-slate-300 px-3 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-50">
        Limpar filtros
      </button>
    </section>
  )
}
