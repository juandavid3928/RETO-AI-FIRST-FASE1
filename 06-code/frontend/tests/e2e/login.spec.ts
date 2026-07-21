import { expect, test } from '@playwright/test'
import { createHmac } from 'node:crypto'

test('registered user signs in, persists the JWT session, and logs out locally', async ({ page }) => {
  const email = `login-${Date.now()}@example.com`
  const password = 'correct horse battery'

  await page.goto('/register')
  await page.getByLabel('Email').fill(email)
  await page.getByLabel('Password', { exact: true }).fill(password)
  await page.getByLabel('Confirm password').fill(password)
  await page.getByRole('button', { name: 'Create account' }).click()
  await expect(page.getByRole('status')).toHaveText('Account created successfully.')

  await page.goto('/login')
  await page.getByLabel('Email').fill(` ${email.toUpperCase()} `)
  await page.getByLabel('Password').fill(password)
  await page.getByRole('button', { name: 'Sign in' }).click()

  await expect(page).toHaveURL(/\/login$/)
  await expect(page.getByText('You are authenticated.')).toBeVisible()
  const storedSession = await page.evaluate(() => localStorage.getItem('portal.auth.session'))
  expect(storedSession).not.toBeNull()
  const session = JSON.parse(storedSession!) as { accessToken: unknown; expiresAt: unknown }
  expect(Object.keys(session).sort()).toEqual(['accessToken', 'expiresAt'])
  expect(typeof session.accessToken).toBe('string')
  const [headerSegment, payloadSegment, signatureSegment] = (session.accessToken as string).split('.')
  expect(headerSegment).toBeTruthy()
  expect(payloadSegment).toBeTruthy()
  expect(signatureSegment).toBeTruthy()
  const header = JSON.parse(Buffer.from(headerSegment, 'base64url').toString()) as { alg: unknown }
  const payload = JSON.parse(Buffer.from(payloadSegment, 'base64url').toString()) as Record<string, unknown>
  expect(header.alg).toBe('HS256')
  expect(Object.keys(payload).sort()).toEqual(['aud', 'exp', 'iat', 'iss', 'sub'])
  expect(payload.iss).toBe('portal-convocatorias-api')
  expect(payload.aud).toBe('portal-convocatorias-web')
  expect((payload.exp as number) - (payload.iat as number)).toBe(1800)
  expect(payload.sub).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i)
  const jwtSecret = process.env.JWT_SECRET
  if (!jwtSecret) throw new Error('JWT_SECRET is required to verify the real E2E token')
  const expectedSignature = createHmac('sha256', Buffer.from(jwtSecret, 'base64url'))
    .update(`${headerSegment}.${payloadSegment}`)
    .digest('base64url')
  expect(signatureSegment).toBe(expectedSignature)
  expect(typeof session.expiresAt).toBe('number')
  expect(session.expiresAt).toBeGreaterThan(Date.now())

  await page.reload()
  await expect(page.getByText('You are authenticated.')).toBeVisible()

  await page.evaluate(() => {
    const key = 'portal.auth.session'
    const current = JSON.parse(localStorage.getItem(key)!) as { accessToken: string; expiresAt: number }
    localStorage.setItem(key, JSON.stringify({ ...current, expiresAt: Date.now() - 1 }))
  })
  await page.reload()
  await expect(page.getByRole('alert')).toHaveText('Your session has expired. Sign in again.')
  expect(await page.evaluate(() => localStorage.getItem('portal.auth.session'))).toBeNull()

  await page.getByLabel('Email').fill(email)
  await page.getByLabel('Password').fill(password)
  await page.getByRole('button', { name: 'Sign in' }).click()
  await expect(page.getByText('You are authenticated.')).toBeVisible()
  await page.getByRole('button', { name: 'Log out' }).click()
  await expect(page.getByRole('button', { name: 'Sign in' })).toBeVisible()
  expect(await page.evaluate(() => localStorage.getItem('portal.auth.session'))).toBeNull()
})
