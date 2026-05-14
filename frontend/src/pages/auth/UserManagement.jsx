import { Plus } from 'lucide-react'
import { useEffect, useState } from 'react'

import { DataTable } from '../../components/DataTable.jsx'
import { FormField, inputClassName } from '../../components/FormField.jsx'
import { RoleBadge } from '../../components/auth/RoleBadge.jsx'
import { createUser, listUsers } from '../../services/authService.js'

const columns = [
  { key: 'username', label: 'Usuario' },
  { key: 'email', label: 'Email' },
  { key: 'nome_completo', label: 'Nome' },
  { key: 'role', label: 'Perfil', render: (row) => <RoleBadge role={row.role} /> },
  { key: 'is_active', label: 'Status', render: (row) => row.is_active ? 'Ativo' : 'Inativo' },
]

export function UserManagement() {
  const [rows, setRows] = useState([])
  const [loading, setLoading] = useState(true)
  const [form, setForm] = useState({ username: '', email: '', password: '', first_name: '', last_name: '', role: 'operacional', cargo: '' })

  async function load() {
    setLoading(true)
    listUsers().then(setRows).finally(() => setLoading(false))
  }

  useEffect(() => {
    load()
  }, [])

  async function handleSubmit(event) {
    event.preventDefault()
    await createUser(form)
    setForm({ username: '', email: '', password: '', first_name: '', last_name: '', role: 'operacional', cargo: '' })
    load()
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Seguranca</p>
        <h2 className="text-2xl font-semibold text-slate-950">Gestao de usuarios</h2>
      </div>
      <form onSubmit={handleSubmit} className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-4">
        <FormField label="Usuario"><input className={inputClassName} value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} required /></FormField>
        <FormField label="Email"><input className={inputClassName} type="email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} required /></FormField>
        <FormField label="Senha"><input className={inputClassName} type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} required /></FormField>
        <FormField label="Perfil">
          <select className={inputClassName} value={form.role} onChange={(event) => setForm({ ...form, role: event.target.value })}>
            {['administrador', 'diretoria', 'financeiro', 'compras', 'estoque', 'fiscal', 'comercial', 'operacional', 'supervisor'].map((role) => <option key={role} value={role}>{role}</option>)}
          </select>
        </FormField>
        <FormField label="Nome"><input className={inputClassName} value={form.first_name} onChange={(event) => setForm({ ...form, first_name: event.target.value })} /></FormField>
        <FormField label="Sobrenome"><input className={inputClassName} value={form.last_name} onChange={(event) => setForm({ ...form, last_name: event.target.value })} /></FormField>
        <FormField label="Cargo"><input className={inputClassName} value={form.cargo} onChange={(event) => setForm({ ...form, cargo: event.target.value })} /></FormField>
        <button className="mt-6 inline-flex h-10 items-center justify-center gap-2 rounded-md bg-midnight px-4 text-sm font-semibold text-white"><Plus className="h-4 w-4" /> Criar</button>
      </form>
      <DataTable columns={columns} rows={rows} loading={loading} emptyMessage="Nenhum usuario encontrado." />
    </div>
  )
}
