import { apiClient } from '../api/client.js'

function normalizeList(data) {
  return data.results ?? data.data ?? []
}

export async function listFiscalCompanies() {
  const { data } = await apiClient.get('/fiscal/empresa/')
  return normalizeList(data)
}

export async function createFiscalCompany(payload) {
  const hasFile = payload.certificado_a1 instanceof File
  const body = hasFile ? new FormData() : payload
  if (hasFile) {
    Object.entries(payload).forEach(([key, value]) => {
      if (value !== null && value !== undefined) body.append(key, value)
    })
  }
  const { data } = await apiClient.post('/fiscal/empresa/', body, hasFile ? { headers: { 'Content-Type': 'multipart/form-data' } } : undefined)
  return data.data ?? data
}

export async function listOperationNatures() {
  const { data } = await apiClient.get('/fiscal/naturezas-operacao/')
  return normalizeList(data)
}

export async function createOperationNature(payload) {
  const { data } = await apiClient.post('/fiscal/naturezas-operacao/', payload)
  return data.data ?? data
}

export async function listFiscalProducts() {
  const { data } = await apiClient.get('/fiscal/produtos-fiscais/')
  return normalizeList(data)
}

export async function listFiscalCustomers() {
  const { data } = await apiClient.get('/fiscal/clientes-fiscais/')
  return normalizeList(data)
}

export async function listNFe() {
  const { data } = await apiClient.get('/fiscal/nfe/')
  return normalizeList(data)
}

export async function getNFe(id) {
  const { data } = await apiClient.get(`/fiscal/nfe/${id}/`)
  return data.data ?? data
}

export async function createNFe(payload) {
  const { data } = await apiClient.post('/fiscal/nfe/', payload)
  return data.data ?? data
}

export async function validateNFe(id) {
  const { data } = await apiClient.post(`/fiscal/nfe/${id}/validar/`)
  return data.data ?? data
}

export async function signNFe(id) {
  const { data } = await apiClient.post(`/fiscal/nfe/${id}/assinar/`)
  return data.data ?? data
}

export async function sendNFe(id) {
  const { data } = await apiClient.post(`/fiscal/nfe/${id}/enviar/`)
  return data.data ?? data
}

export async function cancelNFe(id, justificativa) {
  const { data } = await apiClient.post(`/fiscal/nfe/${id}/cancelar/`, { justificativa })
  return data.data ?? data
}

export function getDanfeUrl(id) {
  return `/api/v1/fiscal/nfe/${id}/danfe/`
}

export function getXmlUrl(id) {
  return `/api/v1/fiscal/nfe/${id}/xml/`
}
