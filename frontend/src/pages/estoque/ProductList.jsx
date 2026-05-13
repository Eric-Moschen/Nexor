import { Plus } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { DataTable } from '../../components/DataTable.jsx'
import { listProducts } from '../../services/stockService.js'

const columns = [
  { key: 'codigo_interno', label: 'Codigo' },
  { key: 'sku', label: 'SKU' },
  { key: 'nome', label: 'Produto' },
  { key: 'categoria_nome', label: 'Categoria' },
  { key: 'unidade_medida_sigla', label: 'Un.' },
  { key: 'estoque_atual', label: 'Saldo' },
  { key: 'estoque_minimo', label: 'Minimo' },
  {
    key: 'is_active',
    label: 'Status',
    render: (row) => (
      <span className={`rounded-md px-2 py-1 text-xs font-medium ${row.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-100 text-slate-600'}`}>
        {row.is_active ? 'Ativo' : 'Inativo'}
      </span>
    ),
  },
]

export function ProductList() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    listProducts()
      .then(setProducts)
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="space-y-5">
      <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-center">
        <div>
          <p className="text-sm font-semibold uppercase text-accent">Estoque</p>
          <h2 className="text-2xl font-semibold text-slate-950">Produtos</h2>
        </div>
        <Link to="/estoque/produtos/novo" className="inline-flex items-center justify-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800">
          <Plus className="h-4 w-4" />
          Novo produto
        </Link>
      </div>
      <DataTable columns={columns} rows={products} loading={loading} emptyMessage="Nenhum produto cadastrado." />
    </div>
  )
}
