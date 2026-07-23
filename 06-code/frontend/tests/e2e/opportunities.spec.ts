import { expect, test } from '@playwright/test'


test('registered user can browse current SECOP opportunities through the private portal API', async ({ page }) => {
  const email = `opportunities-${Date.now()}@example.com`
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
  await page.getByRole('button', { name: 'Explore opportunities' }).click()

  await expect(page).toHaveURL(/\/opportunities$/)
  await expect(page.getByRole('heading', { name: 'Current public opportunities' })).toBeVisible()
  await expect(page.getByText('MUNICIPIO DE BRICEÑO')).toBeVisible()
  await expect(page.getByText('Arrendamiento de vehículo')).toBeVisible()
  await expect(page.getByRole('link', { name: 'View in SECOP' })).toHaveAttribute('href', /community\.secop\.gov\.co/)
  const stored = await page.evaluate(() => localStorage.getItem('portal.auth.session'))
  expect(stored).not.toBeNull()
  expect(stored).not.toContain('CO1.REQ')
})
