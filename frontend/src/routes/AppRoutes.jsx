import { Navigate, Route, Routes } from 'react-router-dom'

import { ERP_MODULES } from '../constants/modules.js'
import { AppLayout } from '../layouts/AppLayout.jsx'
import { Dashboard } from '../pages/Dashboard.jsx'
import { ModulePage } from '../pages/ModulePage.jsx'
import { MovementHistory } from '../pages/estoque/MovementHistory.jsx'
import { ProductForm } from '../pages/estoque/ProductForm.jsx'
import { ProductList } from '../pages/estoque/ProductList.jsx'
import { StockMovement } from '../pages/estoque/StockMovement.jsx'
import { PurchaseOrderDetail } from '../pages/compras/PurchaseOrderDetail.jsx'
import { PurchaseOrderList } from '../pages/compras/PurchaseOrderList.jsx'
import { PurchaseReceipt } from '../pages/compras/PurchaseReceipt.jsx'
import { PurchaseRequestDetail } from '../pages/compras/PurchaseRequestDetail.jsx'
import { PurchaseRequestForm } from '../pages/compras/PurchaseRequestForm.jsx'
import { PurchaseRequestList } from '../pages/compras/PurchaseRequestList.jsx'
import { CashFlow } from '../pages/financeiro/CashFlow.jsx'
import { FinancialDashboard } from '../pages/financeiro/FinancialDashboard.jsx'
import { FinancialEntryForm } from '../pages/financeiro/FinancialEntryForm.jsx'
import { PayableList } from '../pages/financeiro/PayableList.jsx'
import { ReceivableList } from '../pages/financeiro/ReceivableList.jsx'
import { FiscalCompanyConfig } from '../pages/fiscal/FiscalCompanyConfig.jsx'
import { NFeDetail } from '../pages/fiscal/NFeDetail.jsx'
import { NFeForm } from '../pages/fiscal/NFeForm.jsx'
import { NFeList } from '../pages/fiscal/NFeList.jsx'
import { OperationNatureList } from '../pages/fiscal/OperationNatureList.jsx'
import { ServiceOrderDetail } from '../pages/ordensServico/ServiceOrderDetail.jsx'
import { ServiceOrderForm } from '../pages/ordensServico/ServiceOrderForm.jsx'
import { ServiceOrderList } from '../pages/ordensServico/ServiceOrderList.jsx'

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route index element={<Dashboard />} />
        <Route path="estoque" element={<ProductList />} />
        <Route path="estoque/produtos/novo" element={<ProductForm />} />
        <Route path="estoque/movimentacoes" element={<StockMovement />} />
        <Route path="estoque/historico" element={<MovementHistory />} />
        <Route path="compras" element={<PurchaseRequestList />} />
        <Route path="compras/solicitacoes/nova" element={<PurchaseRequestForm />} />
        <Route path="compras/solicitacoes/:id" element={<PurchaseRequestDetail />} />
        <Route path="compras/pedidos" element={<PurchaseOrderList />} />
        <Route path="compras/pedidos/:id" element={<PurchaseOrderDetail />} />
        <Route path="compras/pedidos/:id/recebimento" element={<PurchaseReceipt />} />
        <Route path="financeiro" element={<FinancialDashboard />} />
        <Route path="financeiro/contas-pagar" element={<PayableList />} />
        <Route path="financeiro/contas-receber" element={<ReceivableList />} />
        <Route path="financeiro/cadastro/:type" element={<FinancialEntryForm />} />
        <Route path="financeiro/fluxo-caixa" element={<CashFlow />} />
        <Route path="fiscal" element={<NFeList />} />
        <Route path="fiscal/nfe/nova" element={<NFeForm />} />
        <Route path="fiscal/nfe/:id" element={<NFeDetail />} />
        <Route path="fiscal/empresa" element={<FiscalCompanyConfig />} />
        <Route path="fiscal/naturezas" element={<OperationNatureList />} />
        <Route path="ordens-servico" element={<ServiceOrderList />} />
        <Route path="ordens-servico/nova" element={<ServiceOrderForm />} />
        <Route path="ordens-servico/:id" element={<ServiceOrderDetail />} />
        {ERP_MODULES.filter((module) => !['/estoque', '/compras', '/financeiro', '/fiscal', '/ordens-servico'].includes(module.path)).map((module) => (
          <Route key={module.path} path={module.path.slice(1)} element={<ModulePage module={module} />} />
        ))}
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
