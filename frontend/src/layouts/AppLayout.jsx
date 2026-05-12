import { Outlet } from 'react-router-dom';

import { APP_NAME } from '../constants/app';

export function AppLayout() {
  return (
    <div className="min-h-screen bg-nexor-surface text-nexor-graphite">
      <aside className="fixed inset-y-0 hidden w-72 bg-nexor-navy p-6 text-white lg:block">
        <h1 className="text-2xl font-bold tracking-tight">{APP_NAME}</h1>
        <p className="mt-2 text-sm text-slate-300">ERP modular para operações empresariais.</p>
      </aside>
      <main className="lg:pl-72">
        <div className="mx-auto max-w-7xl p-6">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
