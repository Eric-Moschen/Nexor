import { httpClient } from '../api/httpClient';

export const authService = {
  async login(credentials) {
    const { data } = await httpClient.post('/auth/token/', credentials);
    return data;
  },
  async refresh(refreshToken) {
    const { data } = await httpClient.post('/auth/token/refresh/', { refresh: refreshToken });
    return data;
  },
};
