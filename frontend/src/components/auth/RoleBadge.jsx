export function RoleBadge({ role }) {
  const label = String(role ?? '').replaceAll('_', ' ')
  return <span className="rounded-md bg-sky-50 px-2 py-1 text-xs font-semibold uppercase text-sky-700">{label}</span>
}
