export function TimelineGlobal({ events = [] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white p-4">
      <h2 className="text-base font-semibold text-slate-950">Timeline global</h2>
      <div className="mt-4 space-y-4">
        {events.slice(0, 10).map((event) => (
          <div key={event.id} className="border-l-2 border-violet-200 pl-4">
            <p className="text-sm font-semibold text-slate-900">{event.event_name}</p>
            <p className="text-sm text-slate-600">{event.payload?.message || 'Evento integrado processado.'}</p>
            <p className="mt-1 text-xs text-slate-400">{new Date(event.created_at).toLocaleString('pt-BR')}</p>
          </div>
        ))}
        {!events.length && <p className="text-sm text-slate-500">A timeline sera preenchida conforme os fluxos forem executados.</p>}
      </div>
    </section>
  )
}
