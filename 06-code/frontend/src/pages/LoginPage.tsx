import { FormEvent, useEffect, useRef, useState } from 'react'

import { loginAccount } from '../services/login'

const SESSION_KEY = 'portal.auth.session'

type LoginState =
  | 'idle'
  | 'invalid'
  | 'submitting'
  | 'authenticated'
  | 'invalid_credentials'
  | 'network'
  | 'server'
  | 'storage_error'
  | 'expired'
type FieldErrors = Partial<Record<'email' | 'password', string>>

type RestoredSession = { state: LoginState; message: string; expiresAt: number | null }

const STORAGE_ERROR_MESSAGE = 'Browser storage is unavailable. Enable it and try again.'

function removeStoredSession(): boolean {
  try {
    localStorage.removeItem(SESSION_KEY)
    return true
  } catch {
    return false
  }
}

function hasJwtShape(token: unknown): token is string {
  return typeof token === 'string' && /^[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+$/.test(token)
}

function restoreSession(): RestoredSession {
  let stored: string | null
  try {
    stored = localStorage.getItem(SESSION_KEY)
  } catch {
    return { state: 'storage_error', message: STORAGE_ERROR_MESSAGE, expiresAt: null }
  }
  if (!stored) return { state: 'idle', message: '', expiresAt: null }
  try {
    const parsed = JSON.parse(stored) as { accessToken?: unknown; expiresAt?: unknown }
    if (!hasJwtShape(parsed.accessToken) || typeof parsed.expiresAt !== 'number' || !Number.isFinite(parsed.expiresAt)) {
      return removeStoredSession()
        ? { state: 'idle', message: '', expiresAt: null }
        : { state: 'storage_error', message: STORAGE_ERROR_MESSAGE, expiresAt: null }
    }
    if (parsed.expiresAt <= Date.now()) {
      return removeStoredSession()
        ? { state: 'expired', message: 'Your session has expired. Sign in again.', expiresAt: null }
        : { state: 'storage_error', message: STORAGE_ERROR_MESSAGE, expiresAt: null }
    }
    return { state: 'authenticated', message: '', expiresAt: parsed.expiresAt }
  } catch {
    return removeStoredSession()
      ? { state: 'idle', message: '', expiresAt: null }
      : { state: 'storage_error', message: STORAGE_ERROR_MESSAGE, expiresAt: null }
  }
}

export function LoginPage() {
  const restored = useRef<RestoredSession | null>(null)
  if (restored.current === null) restored.current = restoreSession()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [state, setState] = useState<LoginState>(restored.current.state)
  const [message, setMessage] = useState(restored.current.message)
  const [expiresAt, setExpiresAt] = useState<number | null>(restored.current.expiresAt)
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const requestInFlight = useRef(false)
  const emailRef = useRef<HTMLInputElement>(null)
  const passwordRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (state !== 'authenticated' || expiresAt === null) return
    const remaining = expiresAt - Date.now()
    const timer = window.setTimeout(() => {
      setExpiresAt(null)
      if (removeStoredSession()) {
        setState('expired')
        setMessage('Your session has expired. Sign in again.')
      } else {
        setState('storage_error')
        setMessage(STORAGE_ERROR_MESSAGE)
      }
    }, Math.max(0, remaining))
    return () => window.clearTimeout(timer)
  }, [state, expiresAt])

  function logout() {
    setExpiresAt(null)
    if (removeStoredSession()) {
      setMessage('')
      setState('idle')
    } else {
      setMessage(STORAGE_ERROR_MESSAGE)
      setState('storage_error')
    }
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (requestInFlight.current) return
    setFieldErrors({})

    const trimmedEmail = email.trim()
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmedEmail)) {
      setState('invalid')
      setFieldErrors({ email: 'Enter a valid email address.' })
      queueMicrotask(() => emailRef.current?.focus())
      return
    }
    if (password.length < 1 || password.length > 128) {
      setState('invalid')
      setFieldErrors({ password: 'Password must contain 1 to 128 characters.' })
      queueMicrotask(() => passwordRef.current?.focus())
      return
    }

    requestInFlight.current = true
    setState('submitting')
    setMessage('')
    try {
      const response = await loginAccount({ email: trimmedEmail, password })
      if (response.status === 200) {
        const body = await response.json() as { access_token?: unknown; expires_in?: unknown }
        if (!hasJwtShape(body.access_token) || !Number.isInteger(body.expires_in) || (body.expires_in as number) <= 0) {
          removeStoredSession()
          setState('server')
          setMessage('We could not sign you in. Try again.')
          setPassword('')
          return
        }
        const session = { accessToken: body.access_token, expiresAt: Date.now() + (body.expires_in as number) * 1000 }
        try {
          localStorage.setItem(SESSION_KEY, JSON.stringify(session))
        } catch {
          removeStoredSession()
          setState('storage_error')
          setMessage('Your session could not be saved. Check browser storage and try again.')
          setPassword('')
          return
        }
        setEmail('')
        setPassword('')
        setExpiresAt(session.expiresAt)
        setState('authenticated')
      } else if (response.status === 422) {
        let errors: FieldErrors = {}
        try {
          const body = await response.json() as { error?: { fields?: Record<string, string[]> } }
          errors = {
            email: body.error?.fields?.email?.[0],
            password: body.error?.fields?.password?.[0],
          }
        } catch {
          errors = {}
        }
        const firstError = errors.email ?? errors.password ?? 'Review the highlighted fields.'
        setFieldErrors(errors)
        setMessage(firstError)
        setState('invalid')
        queueMicrotask(() => (errors.email ? emailRef.current : passwordRef.current)?.focus())
        setPassword('')
      } else if (response.status === 401) {
        setState('invalid_credentials')
        setMessage('Invalid email or password.')
        setPassword('')
      } else if (response.status === 503) {
        setState('server')
        setMessage('Sign in is temporarily unavailable.')
        setPassword('')
      } else {
        setState('server')
        setMessage('We could not sign you in. Try again.')
        setPassword('')
      }
    } catch {
      setState('network')
      setMessage('Check your connection and try again.')
      setPassword('')
    } finally {
      requestInFlight.current = false
    }
  }

  if (state === 'authenticated') {
    return (
      <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100" data-state={state}>
        <section className="mx-auto max-w-md rounded-2xl border border-slate-700 bg-slate-900 p-7 shadow-2xl">
          <h1 className="text-3xl font-bold">Sign in</h1>
          <p className="mt-5 rounded-lg bg-emerald-950 p-3 text-emerald-200" role="status">You are authenticated.</p>
          <button className="mt-5 w-full rounded-lg bg-amber-300 px-4 py-3 font-bold text-slate-950" type="button" onClick={logout}>Log out</button>
        </section>
      </main>
    )
  }

  const isSubmitting = state === 'submitting'
  const displayMessage = message || fieldErrors.email || fieldErrors.password

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100" data-state={state}>
      <section className="mx-auto max-w-md rounded-2xl border border-slate-700 bg-slate-900 p-7 shadow-2xl">
        <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-amber-300">Portal de Convocatorias</p>
        <h1 className="text-3xl font-bold">Sign in</h1>
        <p className="mt-2 text-slate-300">Use your account credentials.</p>
        <form className="mt-8 space-y-5" onSubmit={submit} noValidate>
          <label className="block font-medium" htmlFor="login-email">Email</label>
          <input ref={emailRef} id="login-email" className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-950 px-3 py-2 focus:border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-300/30" type="email" autoComplete="username" value={email} onChange={(event) => setEmail(event.target.value)} disabled={isSubmitting} aria-invalid={fieldErrors.email ? true : undefined} aria-describedby={fieldErrors.email ? 'login-email-error' : undefined} required />
          {fieldErrors.email && <span id="login-email-error" className="mt-1 block text-sm text-red-300">{fieldErrors.email}</span>}
          <label className="block font-medium" htmlFor="login-password">Password</label>
          <input ref={passwordRef} id="login-password" className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-950 px-3 py-2 focus:border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-300/30" type="password" autoComplete="current-password" minLength={1} maxLength={128} value={password} onChange={(event) => setPassword(event.target.value)} disabled={isSubmitting} aria-invalid={fieldErrors.password ? true : undefined} aria-describedby={fieldErrors.password ? 'login-password-error' : undefined} required />
          {fieldErrors.password && <span id="login-password-error" className="mt-1 block text-sm text-red-300">{fieldErrors.password}</span>}
          {displayMessage && <p className="rounded-lg bg-red-950 p-3 text-red-200" role="alert">{displayMessage}</p>}
          <button className="w-full rounded-lg bg-amber-300 px-4 py-3 font-bold text-slate-950 hover:bg-amber-200 disabled:cursor-not-allowed disabled:opacity-60" type="submit" disabled={isSubmitting}>{isSubmitting ? 'Signing in…' : 'Sign in'}</button>
        </form>
      </section>
    </main>
  )
}
