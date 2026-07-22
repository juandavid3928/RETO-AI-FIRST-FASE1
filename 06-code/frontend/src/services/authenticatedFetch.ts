import { useCallback } from 'react'

import { useAuthSession } from '../auth/AuthSessionProvider'

export type AuthenticatedFetchErrorKind = 'invalid_request' | 'unauthorized' | 'network' | 'server'

export class AuthenticatedFetchError extends Error {
  constructor(readonly kind: AuthenticatedFetchErrorKind, readonly status?: number) {
    super(kind)
    this.name = 'AuthenticatedFetchError'
  }
}

function isAllowedApiPath(path: string): boolean {
  if (!path.startsWith('/api/') || path.startsWith('//')) return false
  try {
    const resolved = new URL(path, window.location.origin)
    return resolved.origin === window.location.origin && resolved.pathname.startsWith('/api/')
  } catch {
    return false
  }
}

export function useAuthenticatedFetch() {
  const { session, clearSession } = useAuthSession()

  return useCallback(async (path: string, init: RequestInit = {}): Promise<Response> => {
    if (!isAllowedApiPath(path)) throw new AuthenticatedFetchError('invalid_request')
    const headers = new Headers(init.headers)
    if (headers.has('authorization')) throw new AuthenticatedFetchError('invalid_request')
    if (session === null) throw new AuthenticatedFetchError('unauthorized')
    headers.set('Authorization', `Bearer ${session.accessToken}`)

    let response: Response
    try {
      response = await fetch(path, { ...init, headers })
    } catch {
      throw new AuthenticatedFetchError('network')
    }
    if (response.status === 401) {
      clearSession()
      throw new AuthenticatedFetchError('unauthorized')
    }
    if (!response.ok) throw new AuthenticatedFetchError('server', response.status)
    return response
  }, [clearSession, session])
}
