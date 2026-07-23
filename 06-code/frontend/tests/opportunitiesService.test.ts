import { describe, expect, it, vi } from 'vitest'

import { fetchOpportunities, InvalidOpportunitiesPayload } from '../src/services/opportunities'


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

describe('fetchOpportunities', () => {
  it('uses authenticatedFetch against the own API and parses the strict contract', async () => {
    const request = vi.fn().mockResolvedValue(new Response(JSON.stringify(PAGE), { status: 200 }))

    await expect(fetchOpportunities(request)).resolves.toEqual(PAGE)

    expect(request).toHaveBeenCalledWith('/api/v1/opportunities?page=1&page_size=20', { headers: { Accept: 'application/json' } })
  })

  it('rejects malformed contracts', async () => {
    const request = vi.fn().mockResolvedValue(new Response(JSON.stringify({ ...PAGE, filters: [] }), { status: 200 }))

    await expect(fetchOpportunities(request)).rejects.toEqual(expect.any(InvalidOpportunitiesPayload))
  })
})
