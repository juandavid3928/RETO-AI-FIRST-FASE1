export type RegistrationPayload = {
  email: string
  password: string
}

export async function registerAccount(payload: RegistrationPayload): Promise<Response> {
  return fetch('/api/v1/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}
