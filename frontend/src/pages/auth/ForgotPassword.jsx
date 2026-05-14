import { Link } from 'react-router-dom'

export function ForgotPassword() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 px-4">
      <section className="w-full max-w-md rounded-md border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-sm font-semibold uppercase text-accent">Recuperacao preparada</p>
        <h1 className="mt-2 text-xl font-semibold text-slate-950">Esqueci minha senha</h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">Fluxo reservado para envio seguro de link por email quando o servico transacional estiver configurado.</p>
        <Link to="/login" className="mt-5 inline-flex rounded-md bg-midnight px-4 py-2 text-sm font-semibold text-white">Voltar ao login</Link>
      </section>
    </main>
  )
}
