import { Save } from 'lucide-react'
import { useEffect, useState } from 'react'

import { PermissionCheckboxList } from '../../components/auth/PermissionCheckboxList.jsx'
import { RoleBadge } from '../../components/auth/RoleBadge.jsx'
import { listPermissions, listRoles, updateRolePermissions } from '../../services/authService.js'

export function RoleManagement() {
  const [roles, setRoles] = useState([])
  const [permissions, setPermissions] = useState([])
  const [selectedRole, setSelectedRole] = useState(null)
  const [selectedPermissions, setSelectedPermissions] = useState([])
  const [message, setMessage] = useState('')

  async function load() {
    const [roleRows, permissionRows] = await Promise.all([listRoles(), listPermissions()])
    setRoles(roleRows)
    setPermissions(permissionRows)
    if (!selectedRole && roleRows.length) {
      setSelectedRole(roleRows[0])
      setSelectedPermissions(roleRows[0].permissions ?? [])
    }
  }

  useEffect(() => {
    load()
  }, [])

  function chooseRole(role) {
    setSelectedRole(role)
    setSelectedPermissions(role.permissions ?? [])
    setMessage('')
  }

  async function savePermissions() {
    const role = await updateRolePermissions(selectedRole.id, selectedPermissions)
    setSelectedRole(role)
    setSelectedPermissions(role.permissions ?? [])
    setRoles((current) => current.map((item) => item.id === role.id ? role : item))
    setMessage('Permissoes atualizadas com sucesso.')
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Seguranca</p>
        <h2 className="text-2xl font-semibold text-slate-950">Gestao de perfis e permissoes</h2>
      </div>
      <section className="grid gap-5 lg:grid-cols-[280px_1fr]">
        <aside className="rounded-md border border-slate-200 bg-white p-4">
          <div className="space-y-2">
            {roles.map((role) => (
              <button key={role.id} type="button" onClick={() => chooseRole(role)} className={`flex w-full items-center justify-between rounded-md px-3 py-2 text-left text-sm font-semibold ${selectedRole?.id === role.id ? 'bg-midnight text-white' : 'text-slate-700 hover:bg-slate-100'}`}>
                {role.name}
                <RoleBadge role={role.code} />
              </button>
            ))}
          </div>
        </aside>
        <section className="rounded-md border border-slate-200 bg-white p-5">
          <div className="flex items-center justify-between gap-3">
            <div>
              <p className="text-sm font-semibold text-slate-950">{selectedRole?.name ?? 'Perfil'}</p>
              <p className="text-sm text-slate-500">{selectedPermissions.length} permissoes selecionadas</p>
            </div>
            <button onClick={savePermissions} disabled={!selectedRole} className="inline-flex items-center gap-2 rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white disabled:opacity-60">
              <Save className="h-4 w-4" />
              Salvar
            </button>
          </div>
          {message ? <p className="mt-4 rounded-md bg-emerald-50 p-3 text-sm font-medium text-emerald-700">{message}</p> : null}
          <div className="mt-4">
            <PermissionCheckboxList permissions={permissions} selected={selectedPermissions} onChange={setSelectedPermissions} />
          </div>
        </section>
      </section>
    </div>
  )
}
