import { useCallback, useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { AuthenticatedFetchError, useAuthenticatedFetch } from '../services/authenticatedFetch'
import { fetchOpportunities, InvalidOpportunitiesPayload, OpportunityPage } from '../services/opportunities'

type OpportunitiesState =
  | { kind: 'loading' }
  | { kind: 'empty' }
  | { kind: 'external_error' }
  | { kind: 'success'; page: OpportunityPage }

export function OpportunitiesPage() {
  const request = useAuthenticatedFetch()
  const navigate = useNavigate()
  const [state, setState] = useState<OpportunitiesState>({ kind: 'loading' })

  const load = useCallback(async () => {
    setState({ kind: 'loading' })
    try {
      const page = await fetchOpportunities(request)
      setState(page.items.length === 0 ? { kind: 'empty' } : { kind: 'success', page })
    } catch (error) {
      if (error instanceof AuthenticatedFetchError && error.kind === 'unauthorized') {
        navigate('/login', { replace: true })
        return
      }
      if (error instanceof InvalidOpportunitiesPayload || error instanceof AuthenticatedFetchError) {
        setState({ kind: 'external_error' })
        return
      }
      setState({ kind: 'external_error' })
    }
  }, [navigate, request])

  useEffect(() => {
    void load()
  }, [load])

  if (state.kind === 'loading') {
    return <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100"><p role="status">Loading opportunities…</p></main>
  }

  if (state.kind === 'empty') {
    return (
      <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100">
        <section className="mx-auto max-w-3xl rounded-2xl border border-slate-700 bg-slate-900 p-7">
          <h1 className="text-3xl font-bold">Current public opportunities</h1>
          <p className="mt-6">No current opportunities were found.</p>
        </section>
      </main>
    )
  }

  if (state.kind === 'external_error') {
    return (
      <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100">
        <section className="mx-auto max-w-3xl rounded-2xl border border-slate-700 bg-slate-900 p-7">
          <p role="alert">Opportunities are temporarily unavailable. Try again later.</p>
          <button type="button" onClick={() => void load()}>Try again</button>
        </section>
      </main>
    )
  }

  return (
    <main className="min-h-screen bg-slate-950 px-4 py-10 text-slate-100">
      <section className="mx-auto max-w-5xl rounded-2xl border border-slate-700 bg-slate-900 p-7 shadow-2xl">
        <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-amber-300">Portal de Convocatorias</p>
        <h1 className="text-3xl font-bold">Current public opportunities</h1>
        <p className="mt-3 text-sm text-slate-300">Showing current SECOP II opportunities from the approved backend integration.</p>
        <ul className="mt-8 space-y-5">
          {state.page.items.map((item) => (
            <li key={item.id} className="rounded-xl border border-slate-700 bg-slate-950 p-5">
              <p className="text-sm font-semibold text-amber-200">{item.entity_name}</p>
              <h2 className="mt-2 text-xl font-bold">{item.title}</h2>
              <p className="mt-2 text-sm text-slate-300">{item.status ?? 'Estado no informado'} · {item.summary_status ?? item.opening_status}</p>
              <p className="mt-2 text-sm">Fecha límite: <time>{item.closing_at}</time></p>
              {item.estimated_amount_cop !== null && <p className="mt-2 text-sm">Valor estimado: {item.estimated_amount_cop.toLocaleString('en-US')} COP</p>}
              {item.source_url !== null && <a className="mt-4 inline-block text-amber-300 underline" href={item.source_url} target="_blank" rel="noreferrer">View in SECOP</a>}
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
