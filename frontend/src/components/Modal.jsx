export function Modal({ open, title, children, onClose }) {
  if (!open) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 px-4">
      <div className="w-full max-w-lg rounded-md bg-white shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
          <h2 className="text-base font-semibold text-slate-950">{title}</h2>
          <button className="rounded-md px-2 py-1 text-sm text-slate-500 hover:bg-slate-100" onClick={onClose}>
            Fechar
          </button>
        </div>
        <div className="p-5">{children}</div>
      </div>
    </div>
  )
}
