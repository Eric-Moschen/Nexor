import { apiClient } from '../api/client.js'

export async function login(credentials) {
  const { data } = await apiClient.post('/auth/token/', credentials)
  return data
}

export async function refreshToken(refresh) {
  const { data } = await apiClient.post('/auth/token/refresh/', { refresh })
  return data
}
