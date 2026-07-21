import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { act, cleanup, fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { App } from '../src/app/App'

const SESSION_KEY = 'portal.auth.session'

beforeEach(() => {
  localStorage.clear()
  window.history.replaceState({}, '', '/login')
})

afterEach(() => {
  cleanup()
  vi.useRealTimers()
  vi.restoreAllMocks()
  localStorage.clear()
  window.history.replaceState({}, '', '/')
})

function renderLogin() {
  return render(<App />)
}

describe('/login', () => {
  it('renders accessible credential fields with login autocomplete', () => {
    renderLogin()

    expect(screen.getByRole('heading', { name: 'Sign in' })).toBeInTheDocument()
    expect(screen.getByLabelText('Email')).toHaveAttribute('type', 'email')
    expect(screen.getByLabelText('Email')).toHaveAttribute('autocomplete', 'username')
    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'password')
    expect(screen.getByLabelText('Password')).toHaveAttribute('autocomplete', 'current-password')
    expect(screen.getByRole('button', { name: 'Sign in' })).toBeEnabled()
  })

  it('rejects a structurally invalid email accessibly and focuses it without calling the API', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
    renderLogin()
    const user = userEvent.setup()

    await user.type(screen.getByLabelText('Email'), 'not-an-email')
    await user.type(screen.getByLabelText('Password'), 'x')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(screen.getByRole('alert')).toHaveTextContent('Enter a valid email address.')
    expect(screen.getByLabelText('Email')).toHaveAttribute('aria-invalid', 'true')
    expect(screen.getByLabelText('Email')).toHaveAttribute('aria-describedby', 'login-email-error')
    expect(screen.getByLabelText('Email')).toHaveFocus()
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('rejects passwords outside the 1-to-128 boundary and focuses the field', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
    renderLogin()
    const user = userEvent.setup()
    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'x'.repeat(129) } })
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(screen.getByRole('alert')).toHaveTextContent('Password must contain 1 to 128 characters.')
    expect(screen.getByLabelText('Password')).toHaveAttribute('aria-invalid', 'true')
    expect(screen.getByLabelText('Password')).toHaveFocus()
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('submits once, preserves the untrimmed 1-character password, stores the session, and replaces with /profile', async () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000)
    let resolveRequest: (response: Response) => void = () => undefined
    const request = new Promise<Response>((resolve) => { resolveRequest = resolve })
    const fetchMock = vi.spyOn(globalThis, 'fetch')
      .mockReturnValueOnce(request)
      .mockResolvedValueOnce(new Response(JSON.stringify({
        id: '8bb45e10-84cb-4b89-8f75-c27bbb319fe8',
        email: 'person@example.com',
        created_at: '2026-07-21T15:00:00Z',
      }), { status: 200 }))
    renderLogin()
    const user = userEvent.setup()

    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    await user.type(screen.getByLabelText('Password'), ' ')
    await user.dblClick(screen.getByRole('button', { name: 'Sign in' }))

    expect(screen.getByRole('button', { name: 'Signing in…' })).toBeDisabled()
    expect(fetchMock).toHaveBeenCalledTimes(1)
    expect(fetchMock).toHaveBeenCalledWith('/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'person@example.com', password: ' ' }),
    })

    resolveRequest(new Response(JSON.stringify({ access_token: 'aaa.bbb.ccc', token_type: 'bearer', expires_in: 1800 }), { status: 200 }))

    expect(await screen.findByRole('heading', { name: 'Your profile' })).toBeVisible()
    expect(screen.getByRole('button', { name: 'Log out' })).toBeEnabled()
    expect(screen.queryByLabelText('Password')).not.toBeInTheDocument()
    expect(localStorage.getItem(SESSION_KEY)).toBe(JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 1_801_000 }))
    expect(window.location.pathname).toBe('/profile')
  })

  it('trims only the email before validation and submission', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(
      JSON.stringify({ access_token: 'aaa.bbb.ccc', token_type: 'bearer', expires_in: 1800 }),
      { status: 200 },
    ))
    renderLogin()
    const user = userEvent.setup()

    await user.type(screen.getByLabelText('Email'), '  Person@Example.com  ')
    await user.type(screen.getByLabelText('Password'), ' password ')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(globalThis.fetch).toHaveBeenCalledWith('/api/v1/auth/login', expect.objectContaining({
      body: JSON.stringify({ email: 'Person@Example.com', password: ' password ' }),
    }))
  })

  it('treats a malformed 200 token contract as a server error without persisting it', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(
      JSON.stringify({ access_token: 'not-a-jwt', token_type: 'bearer', expires_in: 1800 }),
      { status: 200 },
    ))
    renderLogin()
    const user = userEvent.setup()
    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    await user.type(screen.getByLabelText('Password'), 'password')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('We could not sign you in. Try again.')
    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
  })

  it('treats a non-JSON 200 response as a generic server error and clears the password', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response('not-json', { status: 200 }))
    renderLogin()
    const user = userEvent.setup()
    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    await user.type(screen.getByLabelText('Password'), 'password')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('We could not sign you in. Try again.')
    expect(screen.getByLabelText('Password')).toHaveValue('')
    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
  })

  it.each([
    [{ access_token: 'aaa.bbb.ccc', expires_in: 1800 }, 'missing token_type'],
    [{ access_token: 'aaa.bbb.ccc', token_type: 'Bearer', expires_in: 1800 }, 'non-contract token_type'],
    [{ access_token: 'aaa.bbb.ccc', token_type: 'bearer', expires_in: 1799 }, 'non-contract expires_in'],
  ])('rejects a malformed successful login contract: %s (%s)', async (body, _case) => {
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'old.old.old', expiresAt: Date.now() + 60_000 }))
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify(body), { status: 200 }))
    renderLogin()
    const user = userEvent.setup()
    await user.click(screen.getByRole('button', { name: 'Log out' }))
    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    await user.type(screen.getByLabelText('Password'), 'password')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('We could not sign you in. Try again.')
    expect(screen.getByLabelText('Password')).toHaveValue('')
    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
  })

  it.each([
    [401, {}, 'Invalid email or password.'],
    [503, {}, 'Sign in is temporarily unavailable.'],
    [500, {}, 'We could not sign you in. Try again.'],
  ])('maps HTTP %s to an accessible error state', async (status, body, expectedMessage) => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify(body), { status }))
    renderLogin()
    const user = userEvent.setup()
    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    await user.type(screen.getByLabelText('Password'), 'password')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('alert')).toHaveTextContent(expectedMessage)
    expect(screen.getByLabelText('Password')).toHaveValue('')
    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
  })

  it('maps 422 field errors accessibly and focuses the first invalid field', async () => {
    const body = { error: { fields: { email: ['Email is invalid.'], password: ['Password is invalid.'] } } }
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify(body), { status: 422 }))
    renderLogin()
    const user = userEvent.setup()
    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    await user.type(screen.getByLabelText('Password'), 'password')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Email is invalid.')
    expect(screen.getByLabelText('Email')).toHaveAttribute('aria-describedby', 'login-email-error')
    expect(screen.getByLabelText('Email')).toHaveFocus()
  })

  it('shows network state without exposing exception details', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('secret internal detail'))
    renderLogin()
    const user = userEvent.setup()
    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    await user.type(screen.getByLabelText('Password'), 'password')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Check your connection and try again.')
    expect(screen.getByRole('alert')).not.toHaveTextContent('secret internal detail')
  })

  it('restores a valid session and logs out locally without an API call', async () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000)
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 61_000 }))
    const fetchMock = vi.spyOn(globalThis, 'fetch')
    renderLogin()

    expect(screen.getByRole('status')).toHaveTextContent('You are authenticated.')
    await userEvent.setup().click(screen.getByRole('button', { name: 'Log out' }))

    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
    expect(screen.getByRole('button', { name: 'Sign in' })).toBeEnabled()
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('reports storage_error if logout cannot remove the persisted token', async () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000)
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 61_000 }))
    renderLogin()
    vi.spyOn(Storage.prototype, 'removeItem').mockImplementation(() => { throw new DOMException('denied') })

    await userEvent.setup().click(screen.getByRole('button', { name: 'Log out' }))

    expect(screen.getByRole('alert')).toHaveTextContent('Browser storage is unavailable. Enable it and try again.')
    expect(screen.queryByText('You are authenticated.')).not.toBeInTheDocument()
  })

  it('cleans corrupt storage without authenticating', () => {
    localStorage.setItem(SESSION_KEY, '{not-json')
    renderLogin()

    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
    expect(screen.queryByText('You are authenticated.')).not.toBeInTheDocument()
  })

  it('cleans a stored session whose access token is not JWT-shaped', () => {
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'not-a-jwt', expiresAt: Date.now() + 60_000 }))

    renderLogin()

    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
    expect(screen.getByRole('button', { name: 'Sign in' })).toBeInTheDocument()
  })

  it('cleans an expired restored session and reports expiration', () => {
    vi.spyOn(Date, 'now').mockReturnValue(10_000)
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 9_999 }))
    renderLogin()

    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
    expect(screen.getByRole('alert')).toHaveTextContent('Your session has expired. Sign in again.')
  })

  it('expires an active restored session when its timer elapses', () => {
    vi.useFakeTimers()
    vi.setSystemTime(1_000)
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 2_000 }))
    renderLogin()
    expect(screen.getByRole('status')).toHaveTextContent('You are authenticated.')

    act(() => { vi.advanceTimersByTime(1_000) })

    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
    expect(screen.getByRole('alert')).toHaveTextContent('Your session has expired. Sign in again.')
  })

  it('reports storage_error when a successful session cannot be persisted', async () => {
    vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new DOMException('denied') })
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify({ access_token: 'aaa.bbb.ccc', token_type: 'bearer', expires_in: 1800 }), { status: 200 }))
    renderLogin()
    const user = userEvent.setup()
    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    await user.type(screen.getByLabelText('Password'), 'password')
    await user.click(screen.getByRole('button', { name: 'Sign in' }))

    expect(await screen.findByRole('alert')).toHaveTextContent('Your session could not be saved. Check browser storage and try again.')
    expect(screen.queryByText('You are authenticated.')).not.toBeInTheDocument()
  })

  it('reports storage_error when browser storage cannot be read', () => {
    vi.spyOn(Storage.prototype, 'getItem').mockImplementation(() => { throw new DOMException('denied') })

    renderLogin()

    expect(screen.getByRole('alert')).toHaveTextContent('Browser storage is unavailable. Enable it and try again.')
  })

  it('synchronizes logout received from another tab', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000)
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 61_000 }))
    renderLogin()

    localStorage.removeItem(SESSION_KEY)
    act(() => window.dispatchEvent(new StorageEvent('storage', { key: SESSION_KEY, newValue: null, storageArea: localStorage })))

    expect(screen.getByRole('button', { name: 'Sign in' })).toBeVisible()
    expect(screen.queryByText('You are authenticated.')).not.toBeInTheDocument()
  })

  it('synchronizes a valid session received from another tab', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000)
    renderLogin()

    const stored = JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 61_000 })
    localStorage.setItem(SESSION_KEY, stored)
    act(() => window.dispatchEvent(new StorageEvent('storage', { key: SESSION_KEY, newValue: stored, storageArea: localStorage })))

    expect(screen.getByRole('status')).toHaveTextContent('You are authenticated.')
  })

  it('synchronizes an expired session received from another tab', () => {
    vi.spyOn(Date, 'now').mockReturnValue(10_000)
    renderLogin()

    const stored = JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 9_999 })
    localStorage.setItem(SESSION_KEY, stored)
    act(() => window.dispatchEvent(new StorageEvent('storage', { key: SESSION_KEY, newValue: stored, storageArea: localStorage })))

    expect(screen.getByRole('alert')).toHaveTextContent('Your session has expired. Sign in again.')
    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
  })

  it('detects expiration when a hidden tab becomes visible', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000)
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 61_000 }))
    renderLogin()
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 999 }))
    vi.spyOn(document, 'visibilityState', 'get').mockReturnValue('visible')

    act(() => document.dispatchEvent(new Event('visibilitychange')))

    expect(screen.getByRole('alert')).toHaveTextContent('Your session has expired. Sign in again.')
    expect(localStorage.getItem(SESSION_KEY)).toBeNull()
  })

  it('removes storage and visibility listeners and the expiry timer when unmounted', () => {
    vi.spyOn(Date, 'now').mockReturnValue(1_000)
    localStorage.setItem(SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: 61_000 }))
    const windowAdd = vi.spyOn(window, 'addEventListener')
    const windowRemove = vi.spyOn(window, 'removeEventListener')
    const documentAdd = vi.spyOn(document, 'addEventListener')
    const documentRemove = vi.spyOn(document, 'removeEventListener')
    const clearTimer = vi.spyOn(window, 'clearTimeout')

    const view = renderLogin()
    const storageListener = windowAdd.mock.calls.find(([event]) => event === 'storage')?.[1]
    const visibilityListener = documentAdd.mock.calls.find(([event]) => event === 'visibilitychange')?.[1]
    expect(storageListener).toBeTypeOf('function')
    expect(visibilityListener).toBeTypeOf('function')

    view.unmount()

    expect(windowRemove).toHaveBeenCalledWith('storage', storageListener)
    expect(documentRemove).toHaveBeenCalledWith('visibilitychange', visibilityListener)
    expect(clearTimer).toHaveBeenCalled()
  })
})
