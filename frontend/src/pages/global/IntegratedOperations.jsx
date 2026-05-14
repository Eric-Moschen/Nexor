import { useEffect, useMemo, useState } from 'react'

import { ActivityFeed } from '../../components/global/ActivityFeed.jsx'
import { AuditTable } from '../../components/global/AuditTable.jsx'
import { EventViewer } from '../../components/global/EventViewer.jsx'
import { SystemAlerts } from '../../components/global/SystemAlerts.jsx'
import { TimelineGlobal } from '../../components/global/TimelineGlobal.jsx'
import { globalService } from '../../services/globalService.js'

export function IntegratedOperations() {
  const [events, setEvents] = useState([])
  const [logs, setLogs] = useState([])
  const [notifications, setNotifications] = useState([])

  useEffect(() => {
    Promise.all([
      globalService.listEvents(),
      globalService.listAuditLogs(),
      globalService.listNotifications(),
    ]).then(([eventData, auditData, notificationData]) => {
      setEvents(eventData)
      setLogs(auditData)
      setNotifications(notificationData)
    }).catch(() => {
      setEvents([])
      setLogs([])
      setNotifications([])
    })
  }, [])

  const indicators = useMemo(() => [
    { label: 'Eventos processados', value: events.filter((event) => event.status === 'processed').length },
    { label: 'Alertas abertos', value: notifications.filter((item) => !item.is_read).length },
    { label: 'Logs auditaveis', value: logs.length },
    { label: 'Falhas parciais', value: events.filter((event) => event.status === 'partial').length },
  ], [events, logs, notifications])

  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm font-medium uppercase text-violet-700">Operacao integrada</p>
        <h1 className="text-2xl font-semibold text-slate-950">Centro operacional Nexor</h1>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        {indicators.map((item) => (
          <article key={item.label} className="rounded-md border border-slate-200 bg-white p-4">
            <p className="text-sm text-slate-500">{item.label}</p>
            <p className="mt-2 text-2xl font-semibold text-slate-950">{item.value}</p>
          </article>
        ))}
      </div>

      <SystemAlerts notifications={notifications} />

      <div className="grid gap-6 xl:grid-cols-[1fr_0.9fr]">
        <ActivityFeed events={events} />
        <TimelineGlobal events={events} />
      </div>

      <EventViewer events={events} />
      <AuditTable logs={logs} />
    </div>
  )
}
