import { apiClient } from '../api/client.js'

function normalizeList(data) {
  return data.results ?? data.data ?? []
}

export async function listServiceOrders(params = {}) {
  const { data } = await apiClient.get('/os/', { params })
  return normalizeList(data)
}

export async function getServiceOrder(id) {
  const { data } = await apiClient.get(`/os/${id}/`)
  return data.data ?? data
}

export async function createServiceOrder(payload) {
  const { data } = await apiClient.post('/os/', payload)
  return data.data ?? data
}

export async function runServiceOrderAction(id, action, payload = {}) {
  const { data } = await apiClient.post(`/os/${id}/${action}/`, payload)
  return data.data ?? data
}

export async function addServiceOrderMaterial(id, payload) {
  const { data } = await apiClient.post(`/os/${id}/materiais/`, payload)
  return data.data ?? data
}

export async function addServiceOrderTime(id, payload) {
  const { data } = await apiClient.post(`/os/${id}/apontamentos/`, payload)
  return data.data ?? data
}

export async function listServiceOrderHistory(id) {
  const { data } = await apiClient.get(`/os/${id}/historico/`)
  return normalizeList(data)
}
