import { apiClient } from '../api/client.js'

export async function listProducts() {
  const { data } = await apiClient.get('/estoque/produtos/')
  return data.results ?? data.data ?? []
}

export async function createProduct(payload) {
  const { data } = await apiClient.post('/estoque/produtos/', payload)
  return data
}

export async function listCategories() {
  const { data } = await apiClient.get('/estoque/categorias/')
  return data.results ?? data.data ?? []
}

export async function listUnits() {
  const { data } = await apiClient.get('/estoque/unidades-medida/')
  return data.results ?? data.data ?? []
}

export async function listMovements() {
  const { data } = await apiClient.get('/estoque/movimentacoes/')
  return data.results ?? data.data ?? []
}

export async function registerMovement(type, payload) {
  const { data } = await apiClient.post(`/estoque/movimentacoes/${type}/`, payload)
  return data
}
