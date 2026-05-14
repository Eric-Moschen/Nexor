import { useEffect, useState } from 'react'
import { Bell } from 'lucide-react'

import { globalService } from '../../services/globalService.js'

export function NotificationDropdown() {
  const [open, setOpen] = useState(false)
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    globalService.listNotifications({ is_read: false }).then(setNotifications).catch(() => setNotifications([]))
  }, [])

  async function markRead(id) {
    await globalService.markNotificationRead(id)
    setNotifications((items) => items.filter((item) => item.id !== id))
  }

  return (
    <div className="relative">
      <button onClick={() => setOpen((value) => !value)} className="relative inline-flex h-10 w-10 items-center justify-center rounded-md border border-slate-200 text-slate-600 hover:bg-slate-50" title="Notificacoes">
        <Bell className="h-4 w-4" />
        {notifications.length > 0 && <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-rose-500" />}
      </button>
      {open && (
        <div className="absolute right-0 mt-2 w-80 rounded-md border border-slate-200 bg-white shadow-lg">
          <div className="border-b border-slate-200 px-4 py-3">
            <p className="text-sm font-semibold text-slate-950">Notificacoes</p>
          </div>
          <div className="max-h-96 divide-y divide-slate-100 overflow-y-auto">
            {notifications.slice(0, 8).map((item) => (
              <button key={item.id} onClick={() => markRead(item.id)} className="block w-full px-4 py-3 text-left hover:bg-slate-50">
                <p className="text-sm font-medium text-slate-900">{item.title}</p>
                <p className="mt-1 text-xs text-slate-500">{item.message}</p>
              </button>
            ))}
            {!notifications.length && <p className="px-4 py-6 text-sm text-slate-500">Nenhuma notificacao pendente.</p>}
          </div>
        </div>
      )}
    </div>
  )
}
