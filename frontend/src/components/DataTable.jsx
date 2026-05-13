export function DataTable({ columns, rows, loading, emptyMessage = 'Nenhum registro encontrado.' }) {
  if (loading) {
    return <div className="rounded-md border border-slate-200 bg-white p-6 text-sm text-slate-500">Carregando dados...</div>
  }

  if (!rows.length) {
    return <div className="rounded-md border border-dashed border-slate-300 bg-white p-8 text-center text-sm text-slate-500">{emptyMessage}</div>
  }

  return (
    <div className="overflow-hidden rounded-md border border-slate-200 bg-white shadow-sm">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-sm">
          <thead className="bg-slate-50">
            <tr>
              {columns.map((column) => (
                <th key={column.key} className="px-4 py-3 text-left font-semibold text-slate-600">
                  {column.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rows.map((row) => (
              <tr key={row.id} className="hover:bg-slate-50">
                {columns.map((column) => (
                  <td key={column.key} className="px-4 py-3 text-slate-700">
                    {column.render ? column.render(row) : row[column.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
