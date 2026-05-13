export function ModulePage({ module }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-6 shadow-sm">
      <p className="text-sm font-semibold uppercase text-accent">Modulo</p>
      <h2 className="mt-2 text-2xl font-semibold text-slate-950">{module.name}</h2>
      <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-600">Area preparada para conectar fluxos reais do ERP sem concentrar regras de negocio na interface. As chamadas HTTP devem ficar em services e a autorizacao deve respeitar JWT e RBAC.</p>
    </section>
  )
}
