import { apiClient } from '../api/client.js'

function normalizeList(data) {
  return data.results ?? data.data ?? []
}

export async function listPurchaseRequests(params = {}) {
  const { data } = await apiClient.get('/compras/solicitacoes/', { params })
  return normalizeList(data)
}

export async function getPurchaseRequest(id) {
  const { data } = await apiClient.get(`/compras/solicitacoes/${id}/`)
  return data.data ?? data
}

export async function createPurchaseRequest(payload) {
  const { data } = await apiClient.post('/compras/solicitacoes/', payload)
  return data
}

export async function sendPurchaseRequestToApproval(id) {
  const { data } = await apiClient.post(`/compras/solicitacoes/${id}/enviar-aprovacao/`)
  return data
}

export async function approvePurchaseRequest(id) {
  const { data } = await apiClient.post(`/compras/solicitacoes/${id}/aprovar/`)
  return data
}

export async function rejectPurchaseRequest(id, motivo) {
  const { data } = await apiClient.post(`/compras/solicitacoes/${id}/reprovar/`, { motivo })
  return data
}

export async function convertPurchaseRequestToOrder(id, payload) {
  const { data } = await apiClient.post(`/compras/solicitacoes/${id}/converter-pedido/`, payload)
  return data
}

export async function listPurchaseOrders(params = {}) {
  const { data } = await apiClient.get('/compras/pedidos/', { params })
  return normalizeList(data)
}

export async function getPurchaseOrder(id) {
  const { data } = await apiClient.get(`/compras/pedidos/${id}/`)
  return data.data ?? data
}

export async function receivePurchaseOrderPartial(id, payload) {
  const { data } = await apiClient.post(`/compras/pedidos/${id}/recebimento-parcial/`, payload)
  return data
}

export async function receivePurchaseOrderTotal(id, observacao = '') {
  const { data } = await apiClient.post(`/compras/pedidos/${id}/recebimento-total/`, { observacao })
  return data
}

export async function listSuppliers() {
  const { data } = await apiClient.get('/fornecedores/fornecedores/')
  return normalizeList(data)
}
