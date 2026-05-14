import { apiClient } from '../api/client.js'

function normalizeList(data) {
  return data.results ?? data.data ?? []
}

function normalizeDetail(data) {
  return data.data ?? data
}

export async function listCustomers(params = {}) {
  const { data } = await apiClient.get('/clientes/', { params })
  return normalizeList(data)
}

export async function getCustomer(id) {
  const { data } = await apiClient.get(`/clientes/${id}/`)
  return normalizeDetail(data)
}

export async function createCustomer(payload) {
  const { data } = await apiClient.post('/clientes/', payload)
  return normalizeDetail(data)
}

export async function listCustomerHistory(id) {
  const { data } = await apiClient.get(`/clientes/${id}/historico/`)
  return normalizeList(data)
}

export async function listCustomerInteractions(id) {
  const { data } = await apiClient.get(`/clientes/${id}/interacoes/`)
  return normalizeList(data)
}

export async function createCustomerInteraction(id, payload) {
  const { data } = await apiClient.post(`/clientes/${id}/interacoes/`, payload)
  return normalizeDetail(data)
}

export async function listSuppliers(params = {}) {
  const { data } = await apiClient.get('/fornecedores/', { params })
  return normalizeList(data)
}

export async function createSupplier(payload) {
  const { data } = await apiClient.post('/fornecedores/', payload)
  return normalizeDetail(data)
}

export async function listCrmInteractions(params = {}) {
  const { data } = await apiClient.get('/crm/interacoes/', { params })
  return normalizeList(data)
}

export async function createCrmInteraction(payload) {
  const { data } = await apiClient.post('/crm/interacoes/', payload)
  return normalizeDetail(data)
}

export async function finalizeCrmInteraction(id) {
  const { data } = await apiClient.post(`/crm/interacoes/${id}/finalizar/`)
  return normalizeDetail(data)
}
