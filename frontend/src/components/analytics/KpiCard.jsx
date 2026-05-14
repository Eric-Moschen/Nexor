export function KpiCard({ label, value, tone = 'slate' }) {
  const tones = {
    slate: 'border-slate-200 bg-white text-midnight',
    green: 'border-emerald-100 bg-emerald-50 text-emerald-800',
    amber: 'border-amber-100 bg-amber-50 text-amber-800',
    red: 'border-red-100 bg-red-50 text-red-800',
    blue: 'border-sky-100 bg-sky-50 text-sky-800',
  }

  return (
    <div className={`rounded-md border p-4 shadow-sm ${tones[tone] ?? tones.slate}`}>
      <p className="text-xs font-semibold uppercase text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-semibold">{value}</p>
    </div>
  )
}
