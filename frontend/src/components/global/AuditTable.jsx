export function AuditTable({ logs = [] }) {
  return (
    <section className="rounded-md border border-slate-200 bg-white">
      <div className="border-b border-slate-200 px-4 py-3">
        <h2 className="text-base font-semibold text-slate-950">Auditoria global</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50 text-left text-xs font-semibold uppercase text-slate-500">
            <tr>
              <th className="px-4 py-3">Modulo</th>
              <th className="px-4 py-3">Acao</th>
              <th className="px-4 py-3">Registro</th>
              <th className="px-4 py-3">Usuario</th>
              <th className="px-4 py-3">Data</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {logs.slice(0, 10).map((log) => (
              <tr key={log.id}>
                <td className="px-4 py-3 font-medium text-slate-900">{log.module}</td>
                <td className="px-4 py-3 text-slate-600">{log.action}</td>
                <td className="px-4 py-3 text-slate-600">{log.record_repr || `${log.record_model} #${log.record_id}`}</td>
                <td className="px-4 py-3 text-slate-600">{log.user_display || '-'}</td>
                <td className="px-4 py-3 text-slate-500">{new Date(log.created_at).toLocaleString('pt-BR')}</td>
              </tr>
            ))}
            {!logs.length && (
              <tr>
                <td colSpan="5" className="px-4 py-6 text-center text-slate-500">Nenhum log registrado.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}
