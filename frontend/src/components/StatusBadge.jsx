const toneByStatus = {
  rascunho: 'bg-slate-100 text-slate-700',
  pendente_aprovacao: 'bg-amber-50 text-amber-700',
  aprovada: 'bg-emerald-50 text-emerald-700',
  reprovada: 'bg-red-50 text-red-700',
  convertida_pedido: 'bg-indigo-50 text-indigo-700',
  cancelada: 'bg-slate-200 text-slate-600',
  aberto: 'bg-sky-50 text-sky-700',
  enviado_fornecedor: 'bg-violet-50 text-violet-700',
  parcialmente_recebido: 'bg-amber-50 text-amber-700',
  recebido: 'bg-emerald-50 text-emerald-700',
}

export function StatusBadge({ status }) {
  const label = String(status ?? '').replaceAll('_', ' ')
  return <span className={`rounded-md px-2 py-1 text-xs font-medium ${toneByStatus[status] ?? 'bg-slate-100 text-slate-700'}`}>{label}</span>
}
