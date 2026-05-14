import { NavLink } from 'react-router-dom'
import { Boxes, ChartNoAxesCombined, ClipboardList, FileText, Landmark, LayoutDashboard, MessagesSquare, ReceiptText, ShieldCheck, Truck, Users } from 'lucide-react'

const items = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/dashboard/financeiro', label: 'BI Financeiro', icon: ChartNoAxesCombined },
  { to: '/dashboard/estoque', label: 'BI Estoque', icon: ChartNoAxesCombined },
  { to: '/dashboard/comercial', label: 'BI Comercial', icon: ChartNoAxesCombined },
  { to: '/dashboard/operacional', label: 'BI Operacional', icon: ChartNoAxesCombined },
  { to: '/estoque', label: 'Estoque', icon: Boxes },
  { to: '/estoque/movimentacoes', label: 'Movimentar estoque', icon: ClipboardList },
  { to: '/estoque/historico', label: 'Historico estoque', icon: FileText },
  { to: '/compras', label: 'Compras', icon: ClipboardList },
  { to: '/compras/pedidos', label: 'Pedidos de compra', icon: Truck },
  { to: '/financeiro', label: 'Financeiro', icon: Landmark },
  { to: '/financeiro/contas-pagar', label: 'Contas a pagar', icon: Landmark },
  { to: '/financeiro/contas-receber', label: 'Contas a receber', icon: ReceiptText },
  { to: '/fiscal', label: 'NF-e', icon: ReceiptText },
  { to: '/fiscal/empresa', label: 'Empresa fiscal', icon: ShieldCheck },
  { to: '/fiscal/naturezas', label: 'Naturezas fiscais', icon: FileText },
  { to: '/ordens-servico', label: 'Ordens de Servico', icon: ShieldCheck },
  { to: '/orcamentos', label: 'Orcamentos', icon: FileText },
  { to: '/clientes', label: 'Clientes', icon: Users },
  { to: '/crm', label: 'CRM', icon: MessagesSquare },
  { to: '/fornecedores', label: 'Fornecedores', icon: Truck },
  { to: '/relatorios', label: 'Relatorios', icon: FileText },
]

export function Sidebar() {
  return (
    <aside className="fixed inset-y-0 left-0 hidden w-72 border-r border-slate-200 bg-white lg:block">
      <div className="flex h-16 items-center border-b border-slate-200 px-6">
        <div>
          <p className="text-lg font-semibold text-midnight">Nexor ERP</p>
          <p className="text-xs font-medium uppercase text-slate-500">Operacao empresarial</p>
        </div>
      </div>
      <nav className="space-y-1 px-3 py-4">
        {items.map((item) => {
          const Icon = item.icon
          return (
            <NavLink key={item.to} to={item.to} className={({ isActive }) => `flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition ${isActive ? 'bg-midnight text-white' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-950'}`}>
              <Icon className="h-4 w-4" />
              {item.label}
            </NavLink>
          )
        })}
      </nav>
    </aside>
  )
}
