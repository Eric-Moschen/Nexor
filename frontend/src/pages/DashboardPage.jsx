const modules = ['Estoque', 'Compras', 'Financeiro', 'Fiscal', 'Ordens de Serviço', 'Relatórios'];

export function DashboardPage() {
  return (
    <section>
      <div className="rounded-3xl bg-white p-8 shadow-sm ring-1 ring-slate-200">
        <span className="text-sm font-semibold uppercase tracking-wide text-nexor-purple">Base inicial</span>
        <h2 className="mt-3 text-4xl font-bold text-nexor-navy">Nexor ERP</h2>
        <p className="mt-4 max-w-3xl text-slate-600">
          Estrutura profissional preparada para autenticação JWT, RBAC, domínios desacoplados,
          PostgreSQL, Redis e processamento assíncrono com Celery.
        </p>
      </div>
      <div className="mt-8 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {modules.map((module) => (
          <article key={module} className="rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200">
            <h3 className="font-semibold text-nexor-navy">{module}</h3>
            <p className="mt-2 text-sm text-slate-500">Módulo preparado para evolução incremental.</p>
          </article>
        ))}
      </div>
    </section>
  );
}
