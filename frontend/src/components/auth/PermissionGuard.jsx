import { useAuth } from '../../hooks/useAuth.js'

export function PermissionGuard({ permission, children, fallback = null }) {
  const { hasPermission } = useAuth()
  return hasPermission(permission) ? children : fallback
}
