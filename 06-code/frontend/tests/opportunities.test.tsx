import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { cleanup, render, screen } from '@testing-library/react'

import { App } from '../src/app/App'
import { AUTH_SESSION_KEY } from '../src/auth/authSession'


const PAGE = {
  items: [{
    id: 'CO1.REQ.10658713',
    reference: 'SA-SIE-016-2026',
    entity_name: 'MUNICIPIO DE BRICEÑO',
    title: 'Arrendamiento de vehículo',
    description: 'Contratar el arrendamiento de vehículo',
    status: 'Publicado',
    summary_status: 'Presentación de oferta',
    opening_status: 'Abierto',
    published_at: '2026-07-15T00:00:00.000',
    closing_at: '2026-07-23T00:00:00.000',
    estimated_amount_cop: 77500000,
    source_url: 'https://community.secop.gov.co/Public/Tendering/OpportunityDetail/Index?noticeUID=CO1.NTC.10512397',
  }],
  page: 1,
  page_size: 20,
  has_more: false,
}

beforeEach(() => {
  localStorage.setItem(AUTH_SESSION_KEY, JSON.stringify({ accessToken: 'aaa.bbb.ccc', expiresAt: Date.now() + 60_000 }))
  window.history.replaceState({}, '', '/opportunities')
})

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
  localStorage.clear()
  window.history.replaceState({}, '', '/')
})

describe('/opportunities', () => {
  it('loads current opportunities through authenticatedFetch and shows success without HU-004 filters', async () => {
    const fetchMock = vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify(PAGE), { status: 200 }))

    render(<App />)

    expect(screen.getByRole('status')).toHaveTextContent('Loading opportunities')
    expect(await screen.findByRole('heading', { name: 'Current public opportunities' })).toBeVisible()
    expect(screen.getByText('MUNICIPIO DE BRICEÑO')).toBeVisible()
    expect(screen.getByText('Arrendamiento de vehículo')).toBeVisible()
    expect(screen.getByText(/Presentación de oferta/)).toBeVisible()
    expect(screen.getByText(/2026-07-23/)).toBeVisible()
    expect(screen.getByText(/77,500,000/)).toBeVisible()
    expect(screen.getByRole('link', { name: 'View in SECOP' })).toHaveAttribute('href', PAGE.items[0].source_url)
    expect(screen.queryByLabelText(/entity|status|date|filter/i)).not.toBeInTheDocument()
    expect(fetchMock.mock.calls[0][0]).toBe('/api/v1/opportunities?page=1&page_size=20')
    expect(new Headers(fetchMock.mock.calls[0][1]?.headers).get('Authorization')).toBe('Bearer aaa.bbb.ccc')
    expect(localStorage.getItem(AUTH_SESSION_KEY)).not.toContain('CO1.REQ')
  })

  it('renders an empty state', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(new Response(JSON.stringify({ ...PAGE, items: [] }), { status: 200 }))

    render(<App />)

    expect(await screen.findByText('No current opportunities were found.')).toBeVisible()
  })

  it.each([
    [new Response('{}', { status: 503 })],
    [new Response(JSON.stringify({ ...PAGE, unexpected: true }), { status: 200 })],
  ])('renders an external integration error for server or malformed responses', async (response) => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(response)

    render(<App />)

    expect(await screen.findByRole('alert')).toHaveTextContent('Opportunities are temporarily unavailable')
  })
})
