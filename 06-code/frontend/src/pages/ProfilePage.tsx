import { useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useAuthSession } from '../auth/AuthSessionProvider'
import { AuthenticatedFetchError, useAuthenticatedFetch } from '../services/authenticatedFetch'
import { fetchOwnProfile, OwnProfile } from '../services/profile'

type ProfileState =
  | { kind: 'loading' }
  | { kind: 'success'; profile: OwnProfile }
  | { kind: 'network' }
  | { kind: 'server'; unavailable: boolean }
  | { kind: 'storage_error' }

export function ProfilePage() {
  const auth = useAuthSession()
  const request = useAuthenticatedFetch()
  const navigate = useNavigate()
  const [state, setState] = useState<ProfileState>(() => (
    auth.status === 'storage_error' ? { kind: 'storage_error' } : { kind: 'loading' }
  ))

  const load = useCallback(async () => {
    if (auth.status === 'storage_error') {
      setState({ kind: 'storage_error' })
      return
    }
    if (auth.status !== 'authenticated') return
    setState({ kind: 'loading' })
    try {
      setState({ kind: 'success', profile: await fetchOwnProfile(request) })
    } catch (error) {
      if (error instanceof AuthenticatedFetchError) {
        if (error.kind === 'unauthorized') {
          navigate('/login', { replace: true })
          return
        }
        if (error.kind === 'network') {
          setState({ kind: 'network' })
          return
        }
        setState({ kind: 'server', unavailable: error.status === 503 })
        return
      }
      setState({ kind: 'server', unavailable: false })
    }
  }, [auth.status, navigate, request])

  useEffect(() => {
    void load()
  }, [load])

  function logout() {
    if (auth.clearSession()) navigate('/login', { replace: true })
    else setState({ kind: 'storage_error' })
  }

  if (state.kind === 'loading') {
    return <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100"><p role="status">Loading your profile…</p></main>
  }
  if (state.kind === 'storage_error') {
    return <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100"><p role="alert">Browser storage is unavailable. Enable it and try again.</p></main>
  }
  if (state.kind === 'network' || state.kind === 'server') {
    const message = state.kind === 'network'
      ? 'Check your connection and try again.'
      : state.unavailable ? 'Profile is temporarily unavailable.' : 'We could not load your profile.'
    return (
      <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100">
        <p role="alert">{message}</p>
        <button type="button" onClick={() => void load()}>Try again</button>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100">
      <section className="mx-auto max-w-lg rounded-2xl border border-slate-700 bg-slate-900 p-7 shadow-2xl">
        <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-amber-300">Portal de Convocatorias</p>
        <h1 className="text-3xl font-bold">Your profile</h1>
        <dl className="mt-8 space-y-5">
          <div><dt className="text-sm text-slate-400">Account ID</dt><dd>{state.profile.id}</dd></div>
          <div><dt className="text-sm text-slate-400">Email</dt><dd>{state.profile.email}</dd></div>
          <div><dt className="text-sm text-slate-400">Created at</dt><dd>{state.profile.created_at}</dd></div>
        </dl>
        <button className="mt-8 w-full rounded-lg bg-amber-300 px-4 py-3 font-bold text-slate-950" type="button" onClick={() => navigate('/opportunities')}>Explore opportunities</button>
        <button className="mt-4 w-full rounded-lg border border-slate-600 px-4 py-3 font-bold text-slate-100" type="button" onClick={logout}>Log out</button>
      </section>
    </main>
  )
}
