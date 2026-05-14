import { Link } from 'react-router-dom'

export function AccessDenied() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <section className="w-full max-w-md rounded-md border border-slate-200 bg-white p-6 text-center shadow-sm">
        <p className="text-sm font-semibold uppercase text-red-600">Acesso negado</p>
        <h1 className="mt-2 text-xl font-semibold text-slate-950">Permissao insuficiente</h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">Seu perfil nao possui permissao para acessar esta area.</p>
        <Link to="/" className="mt-5 inline-flex rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white">Ir para dashboard</Link>
      </section>
    </main>
  )
}
