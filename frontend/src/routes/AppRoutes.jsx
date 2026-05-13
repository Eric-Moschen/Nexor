import { Navigate, Route, Routes } from 'react-router-dom'

import { ERP_MODULES } from '../constants/modules.js'
import { AppLayout } from '../layouts/AppLayout.jsx'
import { Dashboard } from '../pages/Dashboard.jsx'
import { ModulePage } from '../pages/ModulePage.jsx'

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Dashboard />} />
        {ERP_MODULES.map((module) => (
          <Route key={module.path} path={module.path.slice(1)} element={<ModulePage module={module} />} />
        ))}
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
