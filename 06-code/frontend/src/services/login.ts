export type LoginPayload = {
  email: string
  password: string
}

export async function loginAccount(payload: LoginPayload): Promise<Response> {
  return fetch('/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
}
