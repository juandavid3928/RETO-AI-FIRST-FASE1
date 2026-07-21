import { act, renderHook } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import type { ReactNode } from 'react'

import { AuthSessionProvider } from '../src/auth/AuthSessionProvider'
import { AUTH_SESSION_KEY } from '../src/auth/authSession'
import { AuthenticatedFetchError, useAuthenticatedFetch } from '../src/services/authenticatedFetch'


const SESSION = { accessToken: 'aaa.bbb.ccc', expiresAt: Date.now() + 60_000 }

function wrapper({ children }: { children: ReactNode }) {
  return <AuthSessionProvider>{children}</AuthSessionProvider>
}

beforeEach(() => {
  localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify(SESSION))
})

afterEach(() => {
  vi.restoreAllMocks()
  localStorage.clear()
})

describe('useAuthenticatedFetch', () => {
  it('adds the central Bearer token to relative API requests', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response('{}', { status: 200 }))
    const { result } = renderHook(() => useAuthenticatedFetch(), { wrapper })

    await act(() => result.current('/api/v1/users/me', { headers: { Accept: 'application/json' } }))

    expect(fetchMock).toHaveBeenCalledTimes(1)
    expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/users/me')
    const headers = new Headers(fetchMock.mock.calls[0][1]?.headers)
    expect(headers.get('Accept')).toBe('application/json')
    expect(headers.get('Authorization')).toBe('Bearer aaa.bbb.ccc')
  })

  it.each([
    'https://evil.example/api/x',
    '//evil.example/api/x',
    '/outside',
    '/api/../outside',
    '/api/%2e%2e/outside',
  ])('rejects a non-API target without sending a token: %s', async (target) => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
    const { result } = renderHook(() => useAuthenticatedFetch(), { wrapper })

    await expect(result.current(target)).rejects.toMatchObject({ kind: 'invalid_request' })
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('rejects caller Authorization overrides without making a request', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
    const { result } = renderHook(() => useAuthenticatedFetch(), { wrapper })

    await expect(result.current('/api/v1/users/me', { headers: { Authorization: 'Bearer attacker' } }))
      .rejects.toMatchObject({ kind: 'invalid_request' })
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('cleans the central session and returns a typed unauthorized error on 401', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response('{}', { status: 401 }))
    const { result } = renderHook(() => useAuthenticatedFetch(), { wrapper })

    await expect(result.current('/api/v1/users/me')).rejects.toEqual(expect.any(AuthenticatedFetchError))
    await expect(result.current('/api/v1/users/me')).rejects.toMatchObject({ kind: 'unauthorized' })
    expect(localStorage.getItem(AUTH_SESSION_KEY)).toBeNull()
  })

  it('returns typed network and server errors without token details', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValueOnce(new TypeError('private network detail'))
    const first = renderHook(() => useAuthenticatedFetch(), { wrapper })
    await expect(first.result.current('/api/v1/users/me')).rejects.toMatchObject({ kind: 'network' })

    vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce(new Response('{}', { status: 503 }))
    const second = renderHook(() => useAuthenticatedFetch(), { wrapper })
    await expect(second.result.current('/api/v1/users/me')).rejects.toMatchObject({ kind: 'server' })
  })
})
