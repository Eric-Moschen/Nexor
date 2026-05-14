import { apiClient } from '../api/client.js'

export async function login(credentials) {
  const { data } = await apiClient.post('/auth/login/', credentials)
  return data.data ?? data
}

export async function refreshToken(refresh) {
  const { data } = await apiClient.post('/auth/refresh/', { refresh })
  return data.data ?? data
}

export async function logout(refresh) {
  const { data } = await apiClient.post('/auth/logout/', { refresh })
  return data.data ?? data
}

export async function getMe() {
  const { data } = await apiClient.get('/auth/me/')
  return data.data ?? data
}

export async function changePassword(payload) {
  const { data } = await apiClient.post('/auth/change-password/', payload)
  return data.data ?? data
}

export async function listUsers() {
  const { data } = await apiClient.get('/accounts/users/')
  return data.results ?? data.data ?? []
}

export async function createUser(payload) {
  const { data } = await apiClient.post('/accounts/users/', payload)
  return data.data ?? data
}

export async function listRoles() {
  const { data } = await apiClient.get('/accounts/roles/')
  return data.results ?? data.data ?? []
}

export async function listPermissions() {
  const { data } = await apiClient.get('/accounts/permissions/')
  return data.results ?? data.data ?? []
}

export async function updateRolePermissions(id, permissions) {
  const { data } = await apiClient.post(`/accounts/roles/${id}/permissions/`, { permissions })
  return data.data ?? data
}
