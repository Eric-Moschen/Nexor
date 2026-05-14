export function PermissionCheckboxList({ permissions, selected, onChange }) {
  function toggle(code) {
    const next = selected.includes(code) ? selected.filter((item) => item !== code) : [...selected, code]
    onChange(next)
  }

  return (
    <div className="grid max-h-80 gap-2 overflow-auto rounded-md border border-slate-200 bg-white p-3 md:grid-cols-2">
      {permissions.map((permission) => (
        <label key={permission.code} className="flex items-center gap-2 text-sm text-slate-700">
          <input type="checkbox" checked={selected.includes(permission.code)} onChange={() => toggle(permission.code)} />
          <span>{permission.code}</span>
        </label>
      ))}
    </div>
  )
}
