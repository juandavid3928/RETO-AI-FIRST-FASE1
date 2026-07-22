import { expect, test } from '@playwright/test'


test('own profile is private, exact, reloadable, and rejects a tampered token', async ({ page }) => {
  const email = `profile-${Date.now()}@example.com`
  const password = 'correct horse battery'

  await page.goto('/register')
  await page.getByLabel('Email').fill(email)
  await page.getByLabel('Password', { exact: true }).fill(password)
  await page.getByLabel('Confirm password').fill(password)
  await page.getByRole('button', { name: 'Create account' }).click()
  await expect(page.getByRole('status')).toHaveText('Account created successfully.')

  await page.goto('/login')
  await page.getByLabel('Email').fill(email)
  await page.getByLabel('Password').fill(password)
  await page.getByRole('button', { name: 'Sign in' }).click()

  await expect(page).toHaveURL(/\/profile$/)
  await expect(page.getByRole('heading', { name: 'Your profile' })).toBeVisible()
  await expect(page.getByText(email)).toBeVisible()
  await expect(page.locator('dt')).toHaveText(['Account ID', 'Email', 'Created at'])
  const stored = await page.evaluate(() => localStorage.getItem('portal.auth.session'))
  expect(stored).not.toBeNull()
  expect(stored).not.toContain(email)

  await page.reload()
  await expect(page.getByText(email)).toBeVisible()

  await page.evaluate(() => {
    const key = 'portal.auth.session'
    const session = JSON.parse(localStorage.getItem(key)!) as { accessToken: string; expiresAt: number }
    const segments = session.accessToken.split('.')
    const signature = segments[2]
    segments[2] = `${signature[0] === 'a' ? 'b' : 'a'}${signature.slice(1)}`
    session.accessToken = segments.join('.')
    localStorage.setItem(key, JSON.stringify(session))
  })
  await page.reload()

  await expect(page).toHaveURL(/\/login$/)
  await expect(page.getByRole('heading', { name: 'Sign in' })).toBeVisible()
  expect(await page.evaluate(() => localStorage.getItem('portal.auth.session'))).toBeNull()
})
