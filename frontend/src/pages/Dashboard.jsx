import { ERP_MODULES } from '../constants/modules.js'

const indicators = [
  ['Modulos estruturados', ERP_MODULES.length],
  ['API versionada', '/api/v1'],
  ['Autenticacao', 'JWT/RBAC'],
  ['Infraestrutura', 'Docker'],
]

export function Dashboard() {
  return (
    <div className="space-y-6">
      <section className="rounded-md border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-sm font-semibold uppercase text-accent">Nexor ERP</p>
        <h2 className="mt-2 text-3xl font-semibold text-slate-950">Estrutura inicial pronta para evolucao modular</h2>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600">Base preparada para operacoes empresariais com dominios separados, seguranca por ambiente e integracao com PostgreSQL, Redis e Celery.</p>
      </section>
      <section className="grid gap-4 md:grid-cols-4">
        {indicators.map(([label, value]) => (
          <div key={label} className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-sm text-slate-500">{label}</p>
            <p className="mt-2 text-2xl font-semibold text-midnight">{value}</p>
          </div>
        ))}
      </section>
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {ERP_MODULES.map((module) => (
          <div key={module.name} className="rounded-md border border-slate-200 bg-white p-4 shadow-sm">
            <p className="text-base font-semibold text-slate-950">{module.name}</p>
            <p className="mt-2 text-sm text-slate-500">Modulo preparado para models, services, selectors, repositories, serializers e views.</p>
            <span className="mt-4 inline-flex rounded-md bg-emerald-50 px-2 py-1 text-xs font-medium text-emerald-700">{module.status}</span>
          </div>
        ))}
      </section>
    </div>
  )
}
