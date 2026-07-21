import { FormEvent, useRef, useState } from 'react'

import { registerAccount } from '../services/register'

type RegistrationState =
  | 'idle'
  | 'invalid'
  | 'submitting'
  | 'success'
  | 'conflict'
  | 'network'
  | 'server'

type FieldErrors = Partial<Record<'email' | 'password' | 'confirmation', string>>

const messages: Partial<Record<RegistrationState, string>> = {
  success: 'Account created successfully.',
  conflict: 'This email is already registered.',
  network: 'Check your connection and try again.',
  server: 'We could not create your account. Try again.',
}

export function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmation, setConfirmation] = useState('')
  const [state, setState] = useState<RegistrationState>('idle')
  const [message, setMessage] = useState('')
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({})
  const requestInFlight = useRef(false)

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (requestInFlight.current) return

    setFieldErrors({})
    const trimmedEmail = email.trim()
    if (!trimmedEmail || !trimmedEmail.includes('@')) {
      setState('invalid')
      setMessage('Enter a valid email address.')
      setFieldErrors({ email: 'Enter a valid email address.' })
      return
    }
    if (password.length < 12 || password.length > 128) {
      setState('invalid')
      setMessage('Password must contain 12 to 128 characters.')
      setFieldErrors({ password: 'Password must contain 12 to 128 characters.' })
      return
    }
    if (password !== confirmation) {
      setState('invalid')
      setMessage('Passwords must match.')
      setFieldErrors({ confirmation: 'Passwords must match.' })
      return
    }

    requestInFlight.current = true
    setState('submitting')
    setMessage('')
    try {
      const response = await registerAccount({ email: trimmedEmail, password })
      if (response.status === 201) {
        setPassword('')
        setConfirmation('')
        setState('success')
        setMessage(messages.success!)
      } else if (response.status === 422) {
        let errors: FieldErrors = {}
        try {
          const body = await response.json() as {
            error?: { fields?: Record<string, string[]> }
          }
          errors = {
            email: body.error?.fields?.email?.[0],
            password: body.error?.fields?.password?.[0],
          }
        } catch {
          errors = {}
        }
        const firstError = errors.email ?? errors.password ?? 'Review the highlighted fields.'
        setFieldErrors(errors)
        setState('invalid')
        setMessage(firstError)
      } else if (response.status === 409) {
        setState('conflict')
        setMessage(messages.conflict!)
      } else if (response.status === 503) {
        setState('server')
        setMessage('Registration is temporarily unavailable.')
      } else {
        setState('server')
        setMessage(messages.server!)
      }
    } catch {
      setState('network')
      setMessage(messages.network!)
    } finally {
      requestInFlight.current = false
    }
  }

  const isSubmitting = state === 'submitting'

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100" data-state={state}>
      <section className="mx-auto max-w-md rounded-2xl border border-slate-700 bg-slate-900 p-7 shadow-2xl">
        <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-amber-300">
          Portal de Convocatorias
        </p>
        <h1 className="text-3xl font-bold">Create your account</h1>
        <p className="mt-2 text-slate-300">Use your email to begin.</p>

        <form className="mt-8 space-y-5" onSubmit={submit} noValidate>
          <label className="block font-medium" htmlFor="email">Email</label>
            <input
              id="email"
              className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-950 px-3 py-2 focus:border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-300/30"
              type="email"
              autoComplete="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              disabled={isSubmitting}
              aria-invalid={fieldErrors.email ? true : undefined}
              aria-describedby={fieldErrors.email ? 'email-error' : undefined}
              required
            />
          {fieldErrors.email && <span id="email-error" className="mt-1 block text-sm text-red-300">{fieldErrors.email}</span>}
          <label className="block font-medium" htmlFor="password">Password</label>
            <input
              id="password"
              className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-950 px-3 py-2 focus:border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-300/30"
              type="password"
              autoComplete="new-password"
              minLength={12}
              maxLength={128}
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              disabled={isSubmitting}
              aria-invalid={fieldErrors.password ? true : undefined}
              aria-describedby={fieldErrors.password ? 'password-help password-error' : 'password-help'}
              required
            />
          {fieldErrors.password && <span id="password-error" className="mt-1 block text-sm text-red-300">{fieldErrors.password}</span>}
          <p id="password-help" className="-mt-3 text-sm text-slate-400">12 to 128 characters.</p>
          <label className="block font-medium" htmlFor="confirmation">Confirm password</label>
            <input
              id="confirmation"
              className="mt-2 w-full rounded-lg border border-slate-600 bg-slate-950 px-3 py-2 focus:border-amber-300 focus:outline-none focus:ring-2 focus:ring-amber-300/30"
              type="password"
              autoComplete="new-password"
              minLength={12}
              maxLength={128}
              value={confirmation}
              onChange={(event) => setConfirmation(event.target.value)}
              disabled={isSubmitting}
              aria-invalid={fieldErrors.confirmation ? true : undefined}
              aria-describedby={fieldErrors.confirmation ? 'confirmation-error' : undefined}
              required
            />
          {fieldErrors.confirmation && <span id="confirmation-error" className="mt-1 block text-sm text-red-300">{fieldErrors.confirmation}</span>}

          {message && (
            <p
              className={state === 'success' ? 'rounded-lg bg-emerald-950 p-3 text-emerald-200' : 'rounded-lg bg-red-950 p-3 text-red-200'}
              role={state === 'success' ? 'status' : 'alert'}
            >
              {message}
            </p>
          )}

          <button
            className="w-full rounded-lg bg-amber-300 px-4 py-3 font-bold text-slate-950 hover:bg-amber-200 disabled:cursor-not-allowed disabled:opacity-60"
            type="submit"
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Creating account…' : 'Create account'}
          </button>
        </form>
      </section>
    </main>
  )
}
