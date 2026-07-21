import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

import { App } from '../src/app/App'

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
  window.history.replaceState({}, '', '/')
})

function renderRegister() {
  window.history.replaceState({}, '', '/register')
  render(<App />)
}

async function fillValidForm() {
  const user = userEvent.setup()
  await user.type(screen.getByLabelText('Email'), ' Person@Example.com ')
  await user.type(screen.getByLabelText('Password'), 'correct horse battery')
  await user.type(screen.getByLabelText('Confirm password'), 'correct horse battery')
  return user
}

describe('/register', () => {
  it('renders only at /register with accessible idle fields', () => {
    renderRegister()
    expect(screen.getByRole('heading', { name: 'Create your account' })).toBeInTheDocument()
    expect(screen.getByLabelText('Email')).toHaveAttribute('type', 'email')
    expect(screen.getByLabelText('Password')).toHaveAttribute('type', 'password')
    expect(screen.getByLabelText('Confirm password')).toHaveAttribute('type', 'password')
    expect(screen.getByRole('button', { name: 'Create account' })).toBeEnabled()
  })

  it('shows invalid state without calling the API for mismatch', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch')
    renderRegister()
    const user = userEvent.setup()
    await user.type(screen.getByLabelText('Email'), 'person@example.com')
    await user.type(screen.getByLabelText('Password'), 'a'.repeat(12))
    await user.type(screen.getByLabelText('Confirm password'), 'b'.repeat(12))
    await user.click(screen.getByRole('button', { name: 'Create account' }))
    expect(screen.getByRole('alert')).toHaveTextContent('Passwords must match.')
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('submits once with email/password only, succeeds, and clears sensitive fields', async () => {
    let resolveRequest: (value: Response) => void = () => undefined
    const request = new Promise<Response>((resolve) => { resolveRequest = resolve })
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockReturnValue(request)
    renderRegister()
    const user = await fillValidForm()
    const submit = screen.getByRole('button', { name: 'Create account' })
    await user.dblClick(submit)
    expect(screen.getByRole('button', { name: 'Creating account…' })).toBeDisabled()
    expect(fetchMock).toHaveBeenCalledTimes(1)
    expect(fetchMock).toHaveBeenCalledWith('/api/v1/auth/register', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ email: 'Person@Example.com', password: 'correct horse battery' }),
    }))
    resolveRequest(new Response(JSON.stringify({ id: crypto.randomUUID() }), { status: 201 }))
    expect(await screen.findByRole('status')).toHaveTextContent('Account created successfully.')
    expect(screen.getByLabelText('Password')).toHaveValue('')
    expect(screen.getByLabelText('Confirm password')).toHaveValue('')
    expect(window.location.pathname).toBe('/register')
  })

  it.each([
    [422, 'Enter a valid email address.'],
    [409, 'This email is already registered.'],
    [503, 'Registration is temporarily unavailable.'],
    [500, 'We could not create your account. Try again.'],
  ])('shows the expected server state for %s', async (status, message) => {
    const body = status === 422
      ? { error: { code: 'validation_error', message: 'Registration data is invalid.', fields: { email: ['Enter a valid email address.'] } } }
      : {}
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify(body), { status }))
    renderRegister()
    const user = await fillValidForm()
    await user.click(screen.getByRole('button', { name: 'Create account' }))
    expect(await screen.findByRole('alert')).toHaveTextContent(message)
    if (status === 422) {
      expect(screen.getByLabelText('Email')).toHaveAttribute('aria-invalid', 'true')
      expect(screen.getByLabelText('Email')).toHaveAttribute('aria-describedby', 'email-error')
    }
  })

  it('shows network state when the API cannot be reached', async () => {
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new TypeError('offline'))
    renderRegister()
    const user = await fillValidForm()
    await user.click(screen.getByRole('button', { name: 'Create account' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Check your connection and try again.')
  })
})
