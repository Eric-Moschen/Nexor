import { createContext, useCallback, useEffect, useMemo, useState } from 'react'

import { getMe, login as loginRequest, logout as logoutRequest } from '../services/authService.js'

export const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(Boolean(localStorage.getItem('nexor.accessToken')))

  const loadUser = useCallback(async () => {
    if (!localStorage.getItem('nexor.accessToken')) {
      setLoading(false)
      return null
    }
    try {
      const me = await getMe()
      setUser(me)
      return me
    } catch {
      setUser(null)
      localStorage.removeItem('nexor.accessToken')
      localStorage.removeItem('nexor.refreshToken')
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadUser()
    const expire = () => setUser(null)
    window.addEventListener('nexor:auth-expired', expire)
    return () => window.removeEventListener('nexor:auth-expired', expire)
  }, [loadUser])

  async function login(credentials) {
    const result = await loginRequest(credentials)
    localStorage.setItem('nexor.accessToken', result.access)
    localStorage.setItem('nexor.refreshToken', result.refresh)
    setUser(result.user)
    return result.user
  }

  async function logout() {
    const refresh = localStorage.getItem('nexor.refreshToken')
    if (refresh) {
      try {
        await logoutRequest(refresh)
      } catch {
        // Local cleanup still protects the browser session if the server already invalidated the token.
      }
    }
    localStorage.removeItem('nexor.accessToken')
    localStorage.removeItem('nexor.refreshToken')
    setUser(null)
  }

  function hasPermission(permission) {
    if (!permission) return true
    if (user?.role === 'administrador') return true
    return Boolean(user?.permissions?.includes(permission))
  }

  const value = useMemo(() => ({ user, loading, login, logout, hasPermission, isAuthenticated: Boolean(user) }), [loading, user])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
