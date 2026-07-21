import { afterEach, describe, expect, it, vi } from 'vitest'

import {
  AUTH_SESSION_KEY,
  clearAuthSession,
  parseLoginResponse,
  readAuthSession,
  saveAuthSession,
} from '../src/auth/authSession'

afterEach(() => {
  vi.restoreAllMocks()
  localStorage.clear()
})

describe('authSession', () => {
  it('accepts only the exact successful login contract', () => {
    expect(parseLoginResponse({
      access_token: 'aaa.bbb.ccc',
      token_type: 'bearer',
      expires_in: 1800,
    }, 1_000)).toEqual({ accessToken: 'aaa.bbb.ccc', expiresAt: 1_801_000 })

    expect(parseLoginResponse({
      access_token: 'aaa.bbb.ccc',
      token_type: 'bearer',
      expires_in: 1800,
      unexpected: true,
    }, 1_000)).toBeNull()
  })

  it('persists and restores a structurally valid unexpired session', () => {
    const session = { accessToken: 'aaa.bbb.ccc', expiresAt: 61_000 }

    expect(saveAuthSession(session)).toBe(true)
    expect(readAuthSession(1_000)).toEqual({ kind: 'authenticated', session })
    expect(localStorage.getItem(AUTH_SESSION_KEY)).toBe(JSON.stringify(session))
  })

  it('rejects and removes a stored session with additional fields', () => {
    localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify({
      accessToken: 'aaa.bbb.ccc',
      expiresAt: 61_000,
      profile: 'not-allowed',
    }))

    expect(readAuthSession(1_000)).toEqual({ kind: 'idle' })
    expect(localStorage.getItem(AUTH_SESSION_KEY)).toBeNull()
  })

  it('removes storage safely when localStorage throws', () => {
    vi.spyOn(Storage.prototype, 'removeItem').mockImplementation(() => { throw new DOMException('denied') })

    expect(clearAuthSession()).toBe(false)
  })

  it('reports read and write storage failures without throwing', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new DOMException('denied') })
    expect(readAuthSession()).toEqual({ kind: 'storage_error' })

    vi.restoreAllMocks()
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new DOMException('denied') })
    expect(saveAuthSession({ accessToken: 'aaa.bbb.ccc', expiresAt: 61_000 })).toBe(false)
  })
})
