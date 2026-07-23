export type Opportunity = {
  id: string
  reference: string | null
  entity_name: string
  title: string
  description: string | null
  status: string | null
  summary_status: string | null
  opening_status: string
  published_at: string | null
  closing_at: string
  estimated_amount_cop: number | null
  source_url: string | null
}

export type OpportunityPage = {
  items: Opportunity[]
  page: number
  page_size: number
  has_more: boolean
}

const PAGE_KEYS = ['has_more', 'items', 'page', 'page_size']
const OPPORTUNITY_KEYS = [
  'closing_at',
  'description',
  'entity_name',
  'estimated_amount_cop',
  'id',
  'opening_status',
  'published_at',
  'reference',
  'source_url',
  'status',
  'summary_status',
  'title',
]

export class InvalidOpportunitiesPayload extends Error {
  constructor() {
    super('invalid_opportunities_payload')
    this.name = 'InvalidOpportunitiesPayload'
  }
}

export async function fetchOpportunities(
  request: (path: string, init?: RequestInit) => Promise<Response>,
  page = 1,
  pageSize = 20,
): Promise<OpportunityPage> {
  const response = await request(`/api/v1/opportunities?page=${page}&page_size=${pageSize}`, { headers: { Accept: 'application/json' } })
  let body: unknown
  try {
    body = await response.json()
  } catch {
    throw new InvalidOpportunitiesPayload()
  }
  if (!isOpportunityPage(body)) throw new InvalidOpportunitiesPayload()
  return body
}

function hasExactKeys(value: Record<string, unknown>, keys: string[]): boolean {
  const actual = Object.keys(value).sort()
  return actual.length === keys.length && actual.every((key, index) => key === keys[index])
}

function isNullableString(value: unknown): value is string | null {
  return value === null || typeof value === 'string'
}

function isOpportunity(value: unknown): value is Opportunity {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false
  const item = value as Record<string, unknown>
  return hasExactKeys(item, OPPORTUNITY_KEYS)
    && typeof item.id === 'string' && item.id.length > 0
    && isNullableString(item.reference)
    && typeof item.entity_name === 'string' && item.entity_name.length > 0
    && typeof item.title === 'string' && item.title.length > 0
    && isNullableString(item.description)
    && isNullableString(item.status)
    && isNullableString(item.summary_status)
    && typeof item.opening_status === 'string' && item.opening_status.length > 0
    && isNullableString(item.published_at)
    && typeof item.closing_at === 'string' && item.closing_at.length > 0
    && (item.estimated_amount_cop === null || (typeof item.estimated_amount_cop === 'number' && Number.isInteger(item.estimated_amount_cop) && item.estimated_amount_cop >= 0))
    && isNullableString(item.source_url)
}

function isOpportunityPage(value: unknown): value is OpportunityPage {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false
  const page = value as Record<string, unknown>
  return hasExactKeys(page, PAGE_KEYS)
    && Array.isArray(page.items)
    && page.items.every(isOpportunity)
    && typeof page.page === 'number' && Number.isInteger(page.page) && page.page >= 1
    && typeof page.page_size === 'number' && Number.isInteger(page.page_size) && page.page_size >= 1 && page.page_size <= 50
    && typeof page.has_more === 'boolean'
}
