import { AlertTriangle } from 'lucide-react'

export function SystemAlerts({ notifications = [] }) {
  const critical = notifications.filter((item) => ['critical', 'warning'].includes(item.level))
  if (!critical.length) {
    return (
      <section className="rounded-md border border-emerald-200 bg-emerald-50 p-4 text-sm font-medium text-emerald-800">
        Operacao sem alertas criticos no momento.
      </section>
    )
  }

  return (
    <section className="space-y-3">
      {critical.slice(0, 4).map((item) => (
        <article key={item.id} className="flex gap-3 rounded-md border border-amber-200 bg-amber-50 p-4">
          <AlertTriangle className="mt-0.5 h-5 w-5 flex-none text-amber-600" />
          <div>
            <h3 className="text-sm font-semibold text-amber-950">{item.title}</h3>
            <p className="text-sm text-amber-800">{item.message}</p>
          </div>
        </article>
      ))}
    </section>
  )
}
