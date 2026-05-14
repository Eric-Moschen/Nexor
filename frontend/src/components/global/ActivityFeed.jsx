import { CheckCircle2, CircleDot } from 'lucide-react'

export function ActivityFeed({ events = [] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white">
      <div className="border-b border-slate-200 px-4 py-3">
        <h2 className="text-base font-semibold text-slate-950">Atividade operacional</h2>
      </div>
      <div className="divide-y divide-slate-100">
        {events.slice(0, 8).map((event) => (
          <article key={event.id} className="flex gap-3 px-4 py-3">
            {event.status === 'processed' ? <CheckCircle2 className="mt-0.5 h-4 w-4 text-emerald-600" /> : <CircleDot className="mt-0.5 h-4 w-4 text-violet-600" />}
            <div>
              <p className="text-sm font-medium text-slate-900">{event.payload?.title || event.event_name}</p>
              <p className="text-xs text-slate-500">{event.module} | {event.aggregate_type} #{event.aggregate_id}</p>
            </div>
          </article>
        ))}
        {!events.length && <p className="px-4 py-6 text-sm text-slate-500">Nenhum evento operacional registrado.</p>}
      </div>
    </section>
  )
}
