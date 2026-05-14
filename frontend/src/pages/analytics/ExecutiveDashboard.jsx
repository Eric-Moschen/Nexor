import { useEffect, useMemo, useState } from 'react'
import { Area, AreaChart, Bar, BarChart, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'

import { KpiCard } from '../../components/analytics/KpiCard.jsx'
import { PeriodFilter } from '../../components/analytics/PeriodFilter.jsx'
import { getDashboard } from '../../services/analyticsService.js'
import { formatCurrency } from '../../utils/formatters.js'

export function ExecutiveDashboard({ type = 'executivo', title = 'Dashboard executivo' }) {
  const [payload, setPayload] = useState(null)
  const [filters, setFilters] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    getDashboard(type, filters).then(setPayload).finally(() => setLoading(false))
  }, [filters, type])

  const indicators = payload?.indicadores ?? {}
  const financeiro = indicators.fluxo_financeiro ?? indicators
  const receitas = financeiro.evolucao_receitas ?? indicators.indicadores_mensais?.financeiro ?? []
  const despesas = financeiro.evolucao_despesas ?? indicators.indicadores_mensais?.despesas ?? []
  const chartData = useMemo(() => receitas.map((row, index) => ({
    periodo: row.periodo,
    receita: Number(row.total ?? 0),
    despesa: Number(despesas[index]?.total ?? 0),
  })), [despesas, receitas])
  const pieData = [
    { name: 'Receber', value: Number(financeiro.contas_receber ?? indicators.total_em_aberto ?? 0) },
    { name: 'Pagar', value: Number(financeiro.contas_pagar ?? 0) },
    { name: 'Recebido', value: Number(financeiro.receita_mensal ?? indicators.total_recebido ?? 0) },
  ]

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Business Intelligence</p>
        <h2 className="text-2xl font-semibold text-slate-950">{title}</h2>
      </div>
      <PeriodFilter filters={filters} onChange={setFilters} />
      {loading ? <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando indicadores...</div> : null}
      {!loading ? (
        <>
          <section className="grid gap-4 md:grid-cols-4">
            <KpiCard label="Faturado" value={formatCurrency(indicators.total_faturado ?? financeiro.receita_mensal)} tone="green" />
            <KpiCard label="Recebido" value={formatCurrency(indicators.total_recebido ?? financeiro.receita_mensal)} tone="blue" />
            <KpiCard label="Em aberto" value={formatCurrency(indicators.total_em_aberto ?? financeiro.contas_receber)} tone="amber" />
            <KpiCard label="OS abertas" value={indicators.total_os_abertas ?? indicators.os_em_execucao ?? 0} />
          </section>
          <section className="grid gap-4 lg:grid-cols-[2fr_1fr]">
            <ChartPanel title="Evolucao financeira">
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="periodo" />
                  <YAxis />
                  <Tooltip />
                  <Area type="monotone" dataKey="receita" stroke="#0f766e" fill="#ccfbf1" />
                  <Area type="monotone" dataKey="despesa" stroke="#b45309" fill="#fef3c7" />
                </AreaChart>
              </ResponsiveContainer>
            </ChartPanel>
            <ChartPanel title="Composicao financeira">
              <ResponsiveContainer width="100%" height={280}>
                <PieChart>
                  <Pie data={pieData} dataKey="value" nameKey="name" outerRadius={90}>
                    {pieData.map((entry, index) => <Cell key={entry.name} fill={['#0ea5e9', '#f59e0b', '#10b981'][index]} />)}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </ChartPanel>
          </section>
          <ChartPanel title="Operacao e comercial">
            <ResponsiveContainer width="100%" height={260}>
              <BarChart data={[
                { name: 'Compras pendentes', value: indicators.total_compras_pendentes ?? 0 },
                { name: 'Orcamentos pendentes', value: indicators.total_orcamentos_pendentes ?? indicators.orcamentos_enviados ?? 0 },
                { name: 'Baixo estoque', value: indicators.produtos_baixo_estoque ?? indicators.produtos_abaixo_minimo ?? 0 },
                { name: 'OS execucao', value: indicators.operacional?.os_em_execucao ?? indicators.os_em_execucao ?? 0 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#4f46e5" />
              </BarChart>
            </ResponsiveContainer>
          </ChartPanel>
        </>
      ) : null}
    </div>
  )
}

function ChartPanel({ title, children }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-5 shadow-sm">
      <h3 className="text-base font-semibold text-slate-950">{title}</h3>
      <div className="mt-4">{children}</div>
    </section>
  )
}
