import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { AuthSessionProvider } from '../auth/AuthSessionProvider'
import { RequireAuth } from '../auth/RequireAuth'
import { LoginPage } from '../pages/LoginPage'
import { OpportunitiesPage } from '../pages/OpportunitiesPage'
import { ProfilePage } from '../pages/ProfilePage'
import { RegisterPage } from '../pages/RegisterPage'

export function App() {
  return (
    <BrowserRouter>
      <AuthSessionProvider>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/profile" element={<RequireAuth><ProfilePage /></RequireAuth>} />
          <Route path="/opportunities" element={<RequireAuth><OpportunitiesPage /></RequireAuth>} />
        </Routes>
      </AuthSessionProvider>
    </BrowserRouter>
  )
}
