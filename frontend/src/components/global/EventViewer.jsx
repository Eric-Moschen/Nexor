export function EventViewer({ events = [] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white">
      <div className="border-b border-slate-200 px-4 py-3">
        <h2 className="text-base font-semibold text-slate-950">Eventos internos</h2>
      </div>
      <div className="grid gap-3 p-4 md:grid-cols-2">
        {events.slice(0, 6).map((event) => (
          <article key={event.id} className="rounded-md border border-slate-200 p-3">
            <div className="flex items-center justify-between gap-3">
              <h3 className="text-sm font-semibold text-slate-900">{event.event_name}</h3>
              <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600">{event.status}</span>
            </div>
            <p className="mt-2 text-sm text-slate-600">{event.payload?.message || event.aggregate_type}</p>
          </article>
        ))}
        {!events.length && <p className="text-sm text-slate-500">Nenhum evento interno disponivel.</p>}
      </div>
    </section>
  )
}
