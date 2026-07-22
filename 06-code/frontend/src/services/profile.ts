export type OwnProfile = {
  id: string
  email: string
  created_at: string
}

const PROFILE_KEYS = ['created_at', 'email', 'id']
const UUID4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i
const UTC_TIMESTAMP = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$/

export class InvalidProfilePayload extends Error {
  constructor() {
    super('invalid_profile_payload')
    this.name = 'InvalidProfilePayload'
  }
}

export async function fetchOwnProfile(request: (path: string, init?: RequestInit) => Promise<Response>): Promise<OwnProfile> {
  const response = await request('/api/v1/users/me', { headers: { Accept: 'application/json' } })
  let body: unknown
  try {
    body = await response.json()
  } catch {
    throw new InvalidProfilePayload()
  }
  if (typeof body !== 'object' || body === null || Array.isArray(body)) throw new InvalidProfilePayload()
  const keys = Object.keys(body).sort()
  if (keys.length !== PROFILE_KEYS.length || keys.some((key, index) => key !== PROFILE_KEYS[index])) {
    throw new InvalidProfilePayload()
  }
  const profile = body as Record<string, unknown>
  if (typeof profile.id !== 'string'
      || !UUID4.test(profile.id)
      || typeof profile.email !== 'string'
      || profile.email.length === 0
      || typeof profile.created_at !== 'string'
      || !UTC_TIMESTAMP.test(profile.created_at)
      || Number.isNaN(Date.parse(profile.created_at))) {
    throw new InvalidProfilePayload()
  }
  return profile as OwnProfile
}
