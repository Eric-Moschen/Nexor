import axios from 'axios';

import { API_BASE_URL } from '../constants/app';

export const httpClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

httpClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('nexor.accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
