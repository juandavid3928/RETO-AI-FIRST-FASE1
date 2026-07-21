import { createContext, ReactNode, useCallback, useContext, useEffect, useMemo, useState } from 'react'

import {
  AuthSession,
  AuthSessionReadResult,
  AUTH_SESSION_KEY,
  clearAuthSession,
  readAuthSession,
  saveAuthSession,
} from './authSession'

export type AuthStatus = 'idle' | 'authenticated' | 'expired' | 'storage_error'

type AuthSessionContextValue = {
  status: AuthStatus
  session: AuthSession | null
  establishSession: (session: AuthSession) => boolean
  clearSession: (status?: 'idle' | 'expired') => boolean
}

const AuthSessionContext = createContext<AuthSessionContextValue | null>(null)

function fromReadResult(result: AuthSessionReadResult): { status: AuthStatus; session: AuthSession | null } {
  return result.kind === 'authenticated'
    ? { status: 'authenticated', session: result.session }
    : { status: result.kind, session: null }
}

export function AuthSessionProvider({ children }: { children: ReactNode }) {
  const [auth, setAuth] = useState(() => fromReadResult(readAuthSession()))

  const synchronize = useCallback(() => {
    setAuth(fromReadResult(readAuthSession()))
  }, [])

  const establishSession = useCallback((session: AuthSession) => {
    if (!saveAuthSession(session)) {
      clearAuthSession()
      setAuth({ status: 'storage_error', session: null })
      return false
    }
    setAuth({ status: 'authenticated', session })
    return true
  }, [])

  const clearSession = useCallback((status: 'idle' | 'expired' = 'idle') => {
    if (!clearAuthSession()) {
      setAuth({ status: 'storage_error', session: null })
      return false
    }
    setAuth({ status, session: null })
    return true
  }, [])

  useEffect(() => {
    const onStorage = (event: StorageEvent) => {
      if (event.key === AUTH_SESSION_KEY || event.key === null) synchronize()
    }
    const onVisibility = () => {
      if (document.visibilityState === 'visible') synchronize()
    }
    window.addEventListener('storage', onStorage)
    document.addEventListener('visibilitychange', onVisibility)
    return () => {
      window.removeEventListener('storage', onStorage)
      document.removeEventListener('visibilitychange', onVisibility)
    }
  }, [synchronize])

  useEffect(() => {
    if (auth.status !== 'authenticated' || auth.session === null) return
    const timer = window.setTimeout(
      () => clearSession('expired'),
      Math.max(0, auth.session.expiresAt - Date.now()),
    )
    return () => window.clearTimeout(timer)
  }, [auth, clearSession])

  const value = useMemo<AuthSessionContextValue>(() => ({
    status: auth.status,
    session: auth.session,
    establishSession,
    clearSession,
  }), [auth, clearSession, establishSession])

  return <AuthSessionContext.Provider value={value}>{children}</AuthSessionContext.Provider>
}

export function useAuthSession(): AuthSessionContextValue {
  const context = useContext(AuthSessionContext)
  if (context === null) throw new Error('useAuthSession must be used within AuthSessionProvider')
  return context
}
