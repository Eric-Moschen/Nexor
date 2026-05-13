import { apiClient } from '../api/client.js'

function normalizeList(data) {
  return data.results ?? data.data ?? []
}

export async function listBudgets(params = {}) {
  const { data } = await apiClient.get('/orcamentos/', { params })
  return normalizeList(data)
}

export async function getBudget(id) {
  const { data } = await apiClient.get(`/orcamentos/${id}/`)
  return data.data ?? data
}

export async function createBudget(payload) {
  const { data } = await apiClient.post('/orcamentos/', payload)
  return data.data ?? data
}

export async function runBudgetAction(id, action, payload = {}) {
  const { data } = await apiClient.post(`/orcamentos/${id}/${action}/`, payload)
  return data.data ?? data
}

export function getBudgetPdfUrl(id) {
  return `/api/v1/orcamentos/${id}/pdf/`
}
