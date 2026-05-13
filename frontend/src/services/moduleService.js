import { apiClient } from '../api/client.js'

export async function listModuleRecords(modulePath) {
  const { data } = await apiClient.get(`/${modulePath}/registros/`)
  return data
}
