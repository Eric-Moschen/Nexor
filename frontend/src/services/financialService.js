import { apiClient } from '../api/client.js'

function normalizeList(data) {
  return data.results ?? data.data ?? []
}

export async function getFinancialDashboard() {
  const { data } = await apiClient.get('/financeiro/dashboard/')
  return data.data ?? data
}

export async function getCashFlow() {
  const { data } = await apiClient.get('/financeiro/fluxo-caixa/')
  return data.data ?? data
}

export async function listPayables(params = {}) {
  const { data } = await apiClient.get('/financeiro/contas-pagar/', { params })
  return normalizeList(data)
}

export async function listReceivables(params = {}) {
  const { data } = await apiClient.get('/financeiro/contas-receber/', { params })
  return normalizeList(data)
}

export async function createPayable(payload) {
  const { data } = await apiClient.post('/financeiro/contas-pagar/', payload)
  return data
}

export async function createReceivable(payload) {
  const { data } = await apiClient.post('/financeiro/contas-receber/', payload)
  return data
}

export async function settlePayable(id, payload) {
  const { data } = await apiClient.post(`/financeiro/contas-pagar/${id}/baixar/`, payload)
  return data
}

export async function settleReceivable(id, payload) {
  const { data } = await apiClient.post(`/financeiro/contas-receber/${id}/baixar/`, payload)
  return data
}

export async function listFinancialCategories() {
  const { data } = await apiClient.get('/financeiro/categorias/')
  return normalizeList(data)
}

export async function listCostCenters() {
  const { data } = await apiClient.get('/financeiro/centros-custo/')
  return normalizeList(data)
}

export async function listCustomers() {
  const { data } = await apiClient.get('/clientes/')
  return normalizeList(data)
}
