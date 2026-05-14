import { apiClient } from '../api/client.js'

const unwrap = (response) => response.data?.results || response.data?.data || response.data || []

export const globalService = {
  async listNotifications(params = {}) {
    const response = await apiClient.get('/notificacoes/', { params })
    return unwrap(response)
  },
  async markNotificationRead(id) {
    const response = await apiClient.post(`/notificacoes/${id}/read/`)
    return response.data?.data || response.data
  },
  async listEvents(params = {}) {
    const response = await apiClient.get('/core/events/', { params })
    return unwrap(response)
  },
  async listAuditLogs(params = {}) {
    const response = await apiClient.get('/auditoria/logs/', { params })
    return unwrap(response)
  },
}
