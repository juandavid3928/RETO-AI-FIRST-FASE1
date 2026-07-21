import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'

import { useAuthSession } from './AuthSessionProvider'

export function RequireAuth({ children }: { children: ReactNode }) {
  const { status } = useAuthSession()
  if (status === 'idle' || status === 'expired') return <Navigate to="/login" replace />
  return children
}
