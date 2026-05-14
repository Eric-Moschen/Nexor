import { ShieldCheck } from 'lucide-react'
import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'

import { FormField, inputClassName } from '../../components/FormField.jsx'
import { useAuth } from '../../hooks/useAuth.js'

export function Login() {
  const [form, setForm] = useState({ username: '', password: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      await login(form)
      navigate(location.state?.from?.pathname ?? '/', { replace: true })
    } catch {
      setError('Credenciais invalidas ou usuario inativo.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <form onSubmit={handleSubmit} className="w-full max-w-md rounded-md border border-slate-200 bg-white p-6 shadow-sm">
        <div className="flex items-center gap-3">
          <span className="inline-flex h-11 w-11 items-center justify-center rounded-md bg-midnight text-white">
            <ShieldCheck className="h-5 w-5" />
          </span>
          <div>
            <p className="text-sm font-semibold uppercase text-accent">Nexor ERP</p>
            <h1 className="text-xl font-semibold text-slate-950">Acesso seguro</h1>
          </div>
        </div>
        {error ? <div className="mt-5 rounded-md border border-red-200 bg-red-50 p-3 text-sm font-medium text-red-700">{error}</div> : null}
        <div className="mt-5 space-y-4">
          <FormField label="Usuario">
            <input className={inputClassName} value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} required />
          </FormField>
          <FormField label="Senha">
            <input className={inputClassName} type="password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} required />
          </FormField>
        </div>
        <button disabled={loading} className="mt-5 w-full rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white hover:bg-slate-800 disabled:opacity-60">
          {loading ? 'Entrando...' : 'Entrar'}
        </button>
        <Link to="/esqueci-senha" className="mt-4 block text-center text-sm font-medium text-accent">Esqueci minha senha</Link>
      </form>
    </main>
  )
}
