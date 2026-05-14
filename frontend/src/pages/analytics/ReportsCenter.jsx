import { Download, FileSpreadsheet, FileText } from 'lucide-react'
import { useEffect, useState } from 'react'

import { DataTable } from '../../components/DataTable.jsx'
import { FormField, inputClassName } from '../../components/FormField.jsx'
import { StatusBadge } from '../../components/StatusBadge.jsx'
import { exportReport, getReport, listExports } from '../../services/analyticsService.js'
import { formatDate } from '../../utils/formatters.js'

const exportColumns = [
  { key: 'tipo_relatorio', label: 'Relatorio' },
  { key: 'formato', label: 'Formato' },
  { key: 'status', label: 'Status', render: (row) => <StatusBadge status={row.status} /> },
  { key: 'created_at', label: 'Gerado em', render: (row) => formatDate(row.created_at) },
  {
    key: 'arquivo_url',
    label: 'Arquivo',
    render: (row) => row.arquivo_url ? <a className="font-semibold text-accent" href={row.arquivo_url}>Download</a> : '-',
  },
]

export function ReportsCenter() {
  const [type, setType] = useState('financeiro')
  const [report, setReport] = useState(null)
  const [exports, setExports] = useState([])
  const [loading, setLoading] = useState(true)

  async function loadData(selectedType = type) {
    setLoading(true)
    const [reportPayload, exportRows] = await Promise.all([getReport(selectedType), listExports()])
    setReport(reportPayload)
    setExports(exportRows)
    setLoading(false)
  }

  useEffect(() => {
    loadData(type)
  }, [type])

  async function handleExport(format) {
    await exportReport(format, { tipo_relatorio: type })
    loadData(type)
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Relatorios</p>
        <h2 className="text-2xl font-semibold text-slate-950">Central de relatorios e exportacoes</h2>
      </div>

      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-[1fr_auto_auto_auto]">
        <FormField label="Tipo de relatorio">
          <select className={inputClassName} value={type} onChange={(event) => setType(event.target.value)}>
            <option value="financeiro">Financeiro</option>
            <option value="estoque">Estoque</option>
            <option value="comercial">Comercial</option>
            <option value="os">Ordens de servico</option>
            <option value="compras">Compras</option>
          </select>
        </FormField>
        <ExportButton icon={FileText} label="PDF" onClick={() => handleExport('pdf')} />
        <ExportButton icon={FileSpreadsheet} label="Excel" onClick={() => handleExport('excel')} />
        <ExportButton icon={Download} label="CSV" onClick={() => handleExport('csv')} />
      </section>

      <section className="rounded-md border border-slate-200 bg-white p-5">
        <h3 className="text-base font-semibold text-slate-950">Resumo analitico</h3>
        {loading ? <p className="mt-4 text-sm text-slate-500">Gerando relatorio...</p> : <pre className="mt-4 max-h-96 overflow-auto rounded-md bg-slate-950 p-4 text-xs text-slate-50">{JSON.stringify(report?.indicadores ?? report, null, 2)}</pre>}
      </section>

      <DataTable columns={exportColumns} rows={exports} loading={loading} emptyMessage="Nenhuma exportacao encontrada." />
    </div>
  )
}

function ExportButton({ icon: Icon, label, onClick }) {
  return (
    <button type="button" onClick={onClick} className="mt-6 inline-flex h-10 items-center justify-center gap-2 rounded-md bg-midnight px-4 text-sm font-semibold text-white hover:bg-slate-800">
      <Icon className="h-4 w-4" />
      {label}
    </button>
  )
}
