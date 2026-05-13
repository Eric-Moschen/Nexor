import { Navigate, Route, Routes } from 'react-router-dom'

import { ERP_MODULES } from '../constants/modules.js'
import { AppLayout } from '../layouts/AppLayout.jsx'
import { Dashboard } from '../pages/Dashboard.jsx'
import { ModulePage } from '../pages/ModulePage.jsx'
import { MovementHistory } from '../pages/estoque/MovementHistory.jsx'
import { ProductForm } from '../pages/estoque/ProductForm.jsx'
import { ProductList } from '../pages/estoque/ProductList.jsx'
import { StockMovement } from '../pages/estoque/StockMovement.jsx'

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="estoque" element={<ProductList />} />
        <Route path="estoque/produtos/novo" element={<ProductForm />} />
        <Route path="estoque/movimentacoes" element={<StockMovement />} />
        <Route path="estoque/historico" element={<MovementHistory />} />
        {ERP_MODULES.filter((module) => module.path !== '/estoque').map((module) => (
          <Route key={module.path} path={module.path.slice(1)} element={<ModulePage module={module} />} />
        ))}
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
