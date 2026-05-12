import { AuthProvider } from './contexts/AuthContext';
import { AppRoutes } from './routes/AppRoutes';

export function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
