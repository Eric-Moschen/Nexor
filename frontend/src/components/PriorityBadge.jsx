const toneByPriority = {
  baixa: 'bg-slate-100 text-slate-700',
  media: 'bg-sky-50 text-sky-700',
  alta: 'bg-amber-50 text-amber-700',
  urgente: 'bg-red-50 text-red-700',
}

export function PriorityBadge({ priority }) {
  const label = String(priority ?? '').replaceAll('_', ' ')
  return <span className={`rounded-md px-2 py-1 text-xs font-medium ${toneByPriority[priority] ?? 'bg-slate-100 text-slate-700'}`}>{label}</span>
}
