import { createContext, useMemo, useState } from 'react';

export const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [session, setSession] = useState(() => ({
    accessToken: localStorage.getItem('nexor.accessToken'),
    refreshToken: localStorage.getItem('nexor.refreshToken'),
  }));

  const value = useMemo(() => ({ session, setSession }), [session]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
