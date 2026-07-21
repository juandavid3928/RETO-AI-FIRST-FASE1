import { type FormEvent, useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useAuthSession } from '../auth/AuthSessionProvider'
import { parseLoginResponse } from '../auth/authSession'
import { loginAccount } from '../services/login'

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

const STORAGE_ERROR_MESSAGE = 'Browser storage is unavailable. Enable it and try again.'
const EXPIRED_MESSAGE = 'Your session has expired. Sign in again.'

function initialState(status: ReturnType<typeof useAuthSession>['status']): { state: LoginState; message: string } {
  if (status === 'authenticated') return { state: 'authenticated', message: '' }
  if (status === 'expired') return { state: 'expired', message: EXPIRED_MESSAGE }
  if (status === 'storage_error') return { state: 'storage_error', message: STORAGE_ERROR_MESSAGE }
  return { state: 'idle', message: '' }
}

export function LoginPage() {
  const auth = useAuthSession()
  const navigate = useNavigate()
  const initial = useRef(initialState(auth.status))
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [state, setState] = useState<LoginState>(initial.current.state)
  const [message, setMessage] = useState(initial.current.message)
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const requestInFlight = useRef(false)
  const emailRef = useRef<HTMLInputElement>(null)
  const passwordRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (auth.status === 'authenticated') {
      setEmail('')
      setPassword('')
      setFieldErrors({})
      setMessage('')
      setState('authenticated')
    } else if (auth.status === 'expired') {
      setPassword('')
      setMessage(EXPIRED_MESSAGE)
      setState('expired')
    } else if (auth.status === 'storage_error' && state !== 'storage_error') {
      setPassword('')
      setMessage(STORAGE_ERROR_MESSAGE)
      setState('storage_error')
    } else if (state === 'authenticated') {
      setPassword('')
      setMessage('')
      setState('idle')
    }
  }, [auth.status, state])

  function logout() {
    if (auth.clearSession()) {
      setMessage('')
      setState('idle')
    } else {
      setMessage(STORAGE_ERROR_MESSAGE)
      setState('storage_error')
    }
  }

  function rejectMalformedLoginResponse() {
    auth.clearSession()
    setState('server')
    setMessage('We could not sign you in. Try again.')
    setPassword('')
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
        let body: unknown
        try {
          body = await response.json()
        } catch {
          rejectMalformedLoginResponse()
          return
        }
        const session = parseLoginResponse(body)
        if (session === null) {
          rejectMalformedLoginResponse()
          return
        }
        if (!auth.establishSession(session)) {
          setState('storage_error')
          setMessage('Your session could not be saved. Check browser storage and try again.')
          setPassword('')
          return
        }
        setEmail('')
        setPassword('')
        navigate('/profile', { replace: true })
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
