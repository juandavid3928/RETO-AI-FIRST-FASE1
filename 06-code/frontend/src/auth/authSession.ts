export const AUTH_SESSION_KEY = 'portal.auth.session'
export const ACCESS_TOKEN_TTL_SECONDS = 1800

export type AuthSession = {
  accessToken: string
  expiresAt: number
}

export type AuthSessionReadResult =
  | { kind: 'idle' }
  | { kind: 'authenticated'; session: AuthSession }
  | { kind: 'expired' }
  | { kind: 'storage_error' }

const JWT_SHAPE = /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/
const LOGIN_RESPONSE_KEYS = ['access_token', 'expires_in', 'token_type']
const STORED_SESSION_KEYS = ['accessToken', 'expiresAt']

function hasJwtShape(value: unknown): value is string {
  return typeof value === 'string' && JWT_SHAPE.test(value)
}

function isAuthSession(value: unknown): value is AuthSession {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false
  const keys = Object.keys(value).sort()
  if (keys.length !== STORED_SESSION_KEYS.length || keys.some((key, index) => key !== STORED_SESSION_KEYS[index])) {
    return false
  }
  const session = value as Partial<AuthSession>
  return hasJwtShape(session.accessToken)
    && typeof session.expiresAt === 'number'
    && Number.isFinite(session.expiresAt)
}

export function parseLoginResponse(value: unknown, now = Date.now()): AuthSession | null {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return null
  const keys = Object.keys(value).sort()
  if (keys.length !== LOGIN_RESPONSE_KEYS.length || keys.some((key, index) => key !== LOGIN_RESPONSE_KEYS[index])) {
    return null
  }
  const response = value as Record<string, unknown>
  if (!hasJwtShape(response.access_token)
      || response.token_type !== 'bearer'
      || response.expires_in !== ACCESS_TOKEN_TTL_SECONDS) {
    return null
  }
  return {
    accessToken: response.access_token,
    expiresAt: now + ACCESS_TOKEN_TTL_SECONDS * 1000,
  }
}

export function clearAuthSession(): boolean {
  try {
    localStorage.removeItem(AUTH_SESSION_KEY)
    return true
  } catch {
    return false
  }
}

export function saveAuthSession(session: AuthSession): boolean {
  try {
    localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify(session))
    return true
  } catch {
    return false
  }
}

export function readAuthSession(now = Date.now()): AuthSessionReadResult {
  let stored: string | null
  try {
    stored = localStorage.getItem(AUTH_SESSION_KEY)
  } catch {
    return { kind: 'storage_error' }
  }
  if (stored === null) return { kind: 'idle' }

  let session: unknown
  try {
    session = JSON.parse(stored)
  } catch {
    return clearAuthSession() ? { kind: 'idle' } : { kind: 'storage_error' }
  }
  if (!isAuthSession(session)) {
    return clearAuthSession() ? { kind: 'idle' } : { kind: 'storage_error' }
  }
  if (session.expiresAt <= now) {
    return clearAuthSession() ? { kind: 'expired' } : { kind: 'storage_error' }
  }
  return { kind: 'authenticated', session }
}
