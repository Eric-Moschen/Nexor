import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import { AppLayout } from '../layouts/AppLayout';
import { DashboardPage } from '../pages/DashboardPage';

const router = createBrowserRouter([
  {
    path: '/',
    element: <AppLayout />,
    children: [{ index: true, element: <DashboardPage /> }],
  },
]);

export function AppRoutes() {
  return <RouterProvider router={router} />;
}
