import { KeyRound } from 'lucide-react'
import { useState } from 'react'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { RoleBadge } from '../../components/auth/RoleBadge.jsx'
import { useAuth } from '../../hooks/useAuth.js'
import { changePassword } from '../../services/authService.js'

export function Profile() {
  const { user } = useAuth()
  const [form, setForm] = useState({ current_password: '', new_password: '' })
  const [message, setMessage] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    await changePassword(form)
    setForm({ current_password: '', new_password: '' })
    setMessage('Senha alterada com sucesso.')
  }

  return (
    <div className="space-y-5">
      <div>
        <p className="text-sm font-semibold uppercase text-accent">Perfil</p>
        <h2 className="text-2xl font-semibold text-slate-950">{user?.nome_completo}</h2>
        <div className="mt-2"><RoleBadge role={user?.role} /></div>
      </div>
      <section className="grid gap-4 rounded-md border border-slate-200 bg-white p-5 md:grid-cols-3">
        <Info label="Email" value={user?.email} />
        <Info label="Telefone" value={user?.telefone || '-'} />
        <Info label="Cargo" value={user?.cargo || '-'} />
      </section>
      <form onSubmit={handleSubmit} className="max-w-xl space-y-4 rounded-md border border-slate-200 bg-white p-5">
        <h3 className="flex items-center gap-2 text-base font-semibold text-slate-950"><KeyRound className="h-4 w-4" /> Alterar senha</h3>
        {message ? <p className="rounded-md bg-emerald-50 p-3 text-sm font-medium text-emerald-700">{message}</p> : null}
        <FormField label="Senha atual">
          <input className={inputClassName} type="password" value={form.current_password} onChange={(event) => setForm({ ...form, current_password: event.target.value })} required />
        </FormField>
        <FormField label="Nova senha">
          <input className={inputClassName} type="password" value={form.new_password} onChange={(event) => setForm({ ...form, new_password: event.target.value })} required />
        </FormField>
        <button className="rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white">Salvar senha</button>
      </form>
    </div>
  )
}

function Info({ label, value }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase text-slate-500">{label}</p>
      <p className="mt-2 text-sm font-semibold text-slate-900">{value}</p>
    </div>
  )
}
