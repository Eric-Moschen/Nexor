import { apiClient } from '../api/client.js'

function normalize(data) {
  return data.data ?? data
}

export async function getDashboard(type, params = {}) {
  const { data } = await apiClient.get(`/dashboard/${type}/`, { params })
  return normalize(data)
}

export async function getReport(type, params = {}) {
  const { data } = await apiClient.get(`/relatorios/${type}/`, { params })
  return normalize(data)
}

export async function exportReport(format, payload) {
  const { data } = await apiClient.post(`/relatorios/exportar/${format}/`, payload)
  return normalize(data)
}

export async function listExports() {
  const { data } = await apiClient.get('/relatorios/exportacoes/')
  return data.results ?? data.data ?? []
}
