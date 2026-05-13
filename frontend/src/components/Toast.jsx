export function Toast({ message, tone = 'success', onClose }) {
  if (!message) return null

  const tones = {
    success: 'border-emerald-200 bg-emerald-50 text-emerald-800',
    error: 'border-red-200 bg-red-50 text-red-800',
  }

  return (
    <div className={`fixed bottom-5 right-5 z-50 flex max-w-sm items-center gap-3 rounded-md border px-4 py-3 text-sm shadow-lg ${tones[tone]}`}>
      <span>{message}</span>
      <button className="text-xs font-semibold" onClick={onClose}>
        OK
      </button>
    </div>
  )
}
