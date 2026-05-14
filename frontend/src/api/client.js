import axios from 'axios'

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api/v1',
  timeout: 15000,
})

let refreshing = null

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('nexor.accessToken')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status !== 401 || originalRequest?._retry) {
      return Promise.reject(error)
    }
    const refresh = localStorage.getItem('nexor.refreshToken')
    if (!refresh) {
      window.dispatchEvent(new Event('nexor:auth-expired'))
      return Promise.reject(error)
    }
    originalRequest._retry = true
    try {
      refreshing = refreshing ?? apiClient.post('/auth/refresh/', { refresh })
      const { data } = await refreshing
      refreshing = null
      const tokens = data.data ?? data
      localStorage.setItem('nexor.accessToken', tokens.access)
      if (tokens.refresh) {
        localStorage.setItem('nexor.refreshToken', tokens.refresh)
      }
      originalRequest.headers.Authorization = `Bearer ${tokens.access}`
      return apiClient(originalRequest)
    } catch (refreshError) {
      refreshing = null
      localStorage.removeItem('nexor.accessToken')
      localStorage.removeItem('nexor.refreshToken')
      window.dispatchEvent(new Event('nexor:auth-expired'))
      return Promise.reject(refreshError)
    }
  },
)
