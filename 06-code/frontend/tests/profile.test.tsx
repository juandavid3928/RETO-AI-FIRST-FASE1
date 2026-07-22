import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { App } from '../src/app/App'
import { AUTH_SESSION_KEY } from '../src/auth/authSession'


const PROFILE = {
  id: '8bb45e10-84cb-4b89-8f75-c27bbb319fe8',
  email: 'person@example.com',
  created_at: '2026-07-21T15:00:00Z',
}

beforeEach(() => {
  localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: Date.now() + 60_000 }))
  window.history.replaceState({}, '', '/profile')
})

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
  localStorage.clear()
  window.history.replaceState({}, '', '/')
})

describe('/profile', () => {
  it('loads and renders only the exact own-profile fields', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify(PROFILE), { status: 200 }))

    render(<App />)

    expect(screen.getByRole('status')).toHaveTextContent('Loading your profile')
    expect(await screen.findByText('person@example.com')).toBeVisible()
    expect(screen.getByText(PROFILE.id)).toBeVisible()
    expect(screen.getByText('2026-07-21T15:00:00Z')).toBeVisible()
    expect(screen.queryByText(/password|token|role|avatar|company|phone/i)).not.toBeInTheDocument()
    expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/users/me')
    expect(new Headers(fetchMock.mock.calls[0][1]?.headers).get('Authorization')).toBe('Bearer aaa.bbb.ccc')
    expect(localStorage.getItem(AUTH_SESSION_KEY)).not.toContain('person@example.com')
  })

  it('cleans the session and replaces the route with login on any 401', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response('{}', { status: 401 }))

    render(<App />)

    expect(await screen.findByRole('heading', { name: 'Sign in' })).toBeVisible()
    expect(window.location.pathname).toBe('/login')
    expect(localStorage.getItem(AUTH_SESSION_KEY)).toBeNull()
  })

  it('shows a retryable network error and succeeds on retry', async () => {
    vi.spyOn(globalThis, 'fetch')
      .mockRejectedValueOnce(new TypeError('offline'))
      .mockResolvedValueOnce(new Response(JSON.stringify(PROFILE), { status: 200 }))

    render(<App />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Check your connection')
    await userEvent.setup().click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByText('person@example.com')).toBeVisible()
  })

  it.each([
    [new Response('{}', { status: 503 }), 'Profile is temporarily unavailable.'],
    [new Response(JSON.stringify({ ...PROFILE, password_hash: 'private' }), { status: 200 }), 'We could not load your profile.'],
  ])('shows a retryable server state for an invalid response', async (response, message) => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(response)

    render(<App />)

    expect(await screen.findByRole('alert')).toHaveTextContent(message)
    expect(screen.getByRole('button', { name: 'Try again' })).toBeEnabled()
  })

  it('shows a controlled storage error without calling the API', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new DOMException('denied') })
    const fetchMock = vi.spyOn(globalThis, 'fetch')

    render(<App />)

    expect(screen.getByRole('alert')).toHaveTextContent('Browser storage is unavailable')
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('redirects an unauthenticated visitor without calling the API', async () => {
    localStorage.clear()
    const fetchMock = vi.spyOn(globalThis, 'fetch')

    render(<App />)

    expect(await screen.findByRole('heading', { name: 'Sign in' })).toBeVisible()
    expect(window.location.pathname).toBe('/login')
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('logs out locally and returns to login', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify(PROFILE), { status: 200 }))
    render(<App />)
    expect(await screen.findByText('person@example.com')).toBeVisible()

    await userEvent.setup().click(screen.getByRole('button', { name: 'Log out' }))

    expect(window.location.pathname).toBe('/login')
    expect(localStorage.getItem(AUTH_SESSION_KEY)).toBeNull()
  })
})
