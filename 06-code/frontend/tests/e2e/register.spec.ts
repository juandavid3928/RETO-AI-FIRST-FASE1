import { expect, test } from '@playwright/test'
import pg from 'pg'

test('browser registration reaches the API and PostgreSQL', async ({ page }) => {
  const databaseUrl = process.env.TEST_DATABASE_URL
  if (!databaseUrl) throw new Error('TEST_DATABASE_URL is required for the real PostgreSQL E2E test')
  const email = `e2e-${crypto.randomUUID()}@example.test`
  const password = 'ephemeral test password'

  await page.goto('/register')
  await page.getByLabel('Email').fill(`  ${email.toUpperCase()}  `)
  await page.getByLabel('Password', { exact: true }).fill(password)
  await page.getByLabel('Confirm password', { exact: true }).fill(password)
  await page.getByRole('button', { name: 'Create account' }).click()

  await expect(page.getByRole('status')).toHaveText('Account created successfully.')
  await expect(page).toHaveURL(/\/register$/)
  await expect(page.getByLabel('Password', { exact: true })).toHaveValue('')
  await expect(page.getByLabel('Confirm password', { exact: true })).toHaveValue('')

  const client = new pg.Client({
    connectionString: databaseUrl,
  })
  await client.connect()
  try {
    const result = await client.query(
      'SELECT email, password_hash FROM users WHERE email = $1',
      [email],
    )
    expect(result.rowCount).toBe(1)
    expect(result.rows[0].password_hash).toMatch(/^\$argon2id\$/)
    expect(result.rows[0].password_hash).not.toContain(password)
  } finally {
    await client.end()
  }
})
