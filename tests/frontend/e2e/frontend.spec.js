import { test, expect } from '@playwright/test'

test.describe('Frontend E2E Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/static/index.html')
  })

  test.describe('Index Page', () => {
    test('should display the page title', async ({ page }) => {
      await expect(page.locator('h2')).toContainText('2025')
    })

    test('should display acciones list', async ({ page }) => {
      const list = page.locator('#acciones-list')
      await expect(list).toBeVisible()
    })

    test('should have year report link', async ({ page }) => {
      const yearLink = page.locator('h2 a')
      await expect(yearLink).toHaveAttribute('href', '/static/cartera_isin.html?year=2025&selected_screen=year_report')
    })

    test('should have load files navigation link', async ({ page }) => {
      const loadFilesLink = page.locator('a[data-navigate="load_files_screen"]')
      await expect(loadFilesLink).toBeVisible()
      await expect(loadFilesLink).toContainText('Load Files')
      const investorDataLink = page.locator('a[data-navigate="investor_data_screen"]')
      await expect(investorDataLink).toContainText('Get MyInvestor Data')
    })
  })

  test.describe('Load Files Screen', () => {
    test('should navigate to load files screen', async ({ page }) => {
      const loadFilesLink = page.locator('a[data-navigate="load_files_screen"]')
      await loadFilesLink.click()

      const loadFilesScreen = page.locator('[data-screen="load_files_screen"]')
      await expect(loadFilesScreen).toBeVisible()
    })

    test('should display load files screen elements', async ({ page }) => {
      const loadFilesLink = page.locator('a[data-navigate="load_files_screen"]')
      await loadFilesLink.click()

      await expect(page.locator('h1')).toContainText('Load All Files')
      await expect(page.locator('#load-files-button')).toBeVisible()
      await expect(page.locator('#load-files-status')).toBeVisible()
      await expect(page.locator('#load-files-output')).toBeVisible()
    })

    test('should have back to home link', async ({ page }) => {
      const loadFilesLink = page.locator('a[data-navigate="load_files_screen"]')
      await loadFilesLink.click()

      const backLink = page.locator('[data-screen="load_files_screen"] a[data-navigate="home"]')
      await expect(backLink).toContainText('← Back to home')
    })

    test('should navigate back to home', async ({ page }) => {
      const loadFilesLink = page.locator('a[data-navigate="load_files_screen"]')
      await loadFilesLink.click()

      const backLink = page.locator('[data-screen="load_files_screen"] a[data-navigate="home"]')
      await backLink.click()

      const homeScreen = page.locator('[data-screen="home"]')
      await expect(homeScreen).toBeVisible()
    })
  })

  test.describe('Investor Data Screen', () => {
    test('should navigate to investor data screen', async ({ page }) => {
      const investorDataLink = page.locator('a[data-navigate="investor_data_screen"]')
      await investorDataLink.click()

      const investorDataScreen = page.locator('[data-screen="investor_data_screen"]')
      await expect(investorDataScreen).toBeVisible()
    })

    test('should display investor data screen elements', async ({ page }) => {
      const investorDataLink = page.locator('a[data-navigate="investor_data_screen"]')
      await investorDataLink.click()

      await expect(page.locator('h1')).toContainText('Get MyInvestor Data')
      await expect(page.locator('#investor-data-form')).toBeVisible()
      await expect(page.locator('input[name="username"]')).toBeVisible()
      await expect(page.locator('input[name="password"]')).toBeVisible()
      await expect(page.locator('#get-investor-data-button')).toBeVisible()
      await expect(page.locator('#investor-data-status')).toBeVisible()
      await expect(page.locator('#investor-data-output')).toBeVisible()
    })

    test('should have back to home link', async ({ page }) => {
      const investorDataLink = page.locator('a[data-navigate="investor_data_screen"]')
      await investorDataLink.click()

      const backLink = page.locator('[data-screen="investor_data_screen"] a[data-navigate="home"]')
      await expect(backLink).toContainText('← Back to home')
    })

    test('should navigate back to home', async ({ page }) => {
      const investorDataLink = page.locator('a[data-navigate="investor_data_screen"]')
      await investorDataLink.click()

      const backLink = page.locator('[data-screen="investor_data_screen"] a[data-navigate="home"]')
      await backLink.click()

      const homeScreen = page.locator('[data-screen="home"]')
      await expect(homeScreen).toBeVisible()
    })

    test('should validate form inputs', async ({ page }) => {
      const investorDataLink = page.locator('a[data-navigate="investor_data_screen"]')
      await investorDataLink.click()

      // Try to submit empty form
      await page.locator('#get-investor-data-button').click()

      // Should show alert (we can't test alert content in e2e, but form should prevent submission)
      // The form should remain visible
      await expect(page.locator('#investor-data-form')).toBeVisible()
    })

    test('should have proper form attributes', async ({ page }) => {
      const investorDataLink = page.locator('a[data-navigate="investor_data_screen"]')
      await investorDataLink.click()

      const usernameInput = page.locator('input[name="username"]')
      const passwordInput = page.locator('input[name="password"]')

      await expect(usernameInput).toHaveAttribute('type', 'text')
      await expect(usernameInput).toHaveAttribute('required')

      await expect(passwordInput).toHaveAttribute('type', 'password')
      await expect(passwordInput).toHaveAttribute('required')
    })
  })

  test.describe('Stock Navigation', () => {
    test('should navigate to stock detail when clicking on a stock', async ({ page }) => {
      await page.waitForSelector('#acciones-list a')
      
      const firstStock = page.locator('#acciones-list a').first()
      const stockName = await firstStock.textContent()
      
      await firstStock.click()
      
      await expect(page).toHaveURL(/\/static\/cartera_isin\.html/)
      await expect(page).toHaveURL(/selected_screen=cartera_accion/)
      await expect(page).toHaveURL(/isin=/)
    })
  })

  test.describe('Cartera Accion Screen', () => {
    test('should navigate to stock detail with correct parameters', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?isin=US5949724083&selected_screen=cartera_accion')
      
      await expect(page).toHaveURL(/isin=US5949724083/)
      await expect(page).toHaveURL(/selected_screen=cartera_accion/)
    })

    test('should display loading state initially', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?isin=US5949724083&selected_screen=cartera_accion')
      
      const loading = page.locator('.c-loading')
      await expect(loading).toBeVisible()
    })

    test('should display stock information after loading', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?isin=US5949724083&selected_screen=cartera_accion')
      
      await page.waitForLoadState('networkidle')
      
      const content = page.locator('.cartera-content')
      await expect(content).toBeVisible()
    })

    test('should display operaciones table', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?isin=US5949724083&selected_screen=cartera_accion')
      
      await page.waitForLoadState('networkidle')
      
      const table = page.locator('.operaciones-tbody')
      await expect(table).toBeVisible()
    })
  })

  test.describe('Year Report Screen', () => {
    test('should navigate to year report', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?year=2024&selected_screen=year_report')
      
      await expect(page).toHaveURL(/year=2024/)
      await expect(page).toHaveURL(/selected_screen=year_report/)
    })

    test('should display year title', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?year=2024&selected_screen=year_report')
      
      await page.waitForLoadState('networkidle')
      
      const yearTitle = page.locator('.year-title')
      await expect(yearTitle).toBeVisible()
      await expect(yearTitle).toHaveText('2024')
    })

    test('should display compra-ventas table', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?year=2024&selected_screen=year_report')
      
      await page.waitForLoadState('networkidle')
      
      const table = page.locator('.compra-ventas-tbody')
      await expect(table).toBeVisible()
    })

    test('should display dividendos table', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?year=2024&selected_screen=year_report')
      
      await page.waitForLoadState('networkidle')
      
      const dividendosTable = page.locator('.dividendos-tbody')
      await expect(dividendosTable).toBeVisible()
    })
  })

  test.describe('URL Parameter Handling', () => {
    test('should handle no_screen when no parameters', async ({ page }) => {
      await page.goto('/static/cartera_isin.html')
      
      const noScreen = page.locator('[data-screen="no_screen"]')
      await expect(noScreen).toBeVisible()
    })

    test('should switch between screens via URL', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?selected_screen=cartera_accion&isin=US5949724083')
      await page.waitForLoadState('networkidle')
      await expect(page.locator('[data-screen="cartera_accion"]')).toBeVisible()
      
      await page.goto('/static/cartera_isin.html?selected_screen=year_report&year=2024')
      await page.waitForLoadState('networkidle')
      await expect(page.locator('[data-screen="year_report"]')).toBeVisible()
    })
  })

  test.describe('Error Handling', () => {
    test('should handle invalid ISIN gracefully', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?isin=INVALID_ISIN&selected_screen=cartera_accion')
      
      await page.waitForLoadState('networkidle')
      
      const error = page.locator('.c-error')
      await expect(error).toBeVisible()
    })

    test('should handle invalid year gracefully', async ({ page }) => {
      await page.goto('/static/cartera_isin.html?year=9999&selected_screen=year_report')
      
      await page.waitForLoadState('networkidle')
      
      const error = page.locator('.c-error')
      await expect(error).toBeVisible()
    })
  })

  test.describe('Responsive Design', () => {
    test('should display correctly on mobile', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 })
      await page.goto('/static/index.html')
      
      await expect(page.locator('h2')).toBeVisible()
      await expect(page.locator('#acciones-list')).toBeVisible()
    })

    test('should display correctly on tablet', async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 })
      await page.goto('/static/index.html')
      
      await expect(page.locator('h2')).toBeVisible()
      await expect(page.locator('#acciones-list')).toBeVisible()
    })

    test('should display correctly on desktop', async ({ page }) => {
      await page.setViewportSize({ width: 1920, height: 1080 })
      await page.goto('/static/index.html')
      
      await expect(page.locator('h2')).toBeVisible()
      await expect(page.locator('#acciones-list')).toBeVisible()
    })
  })

  test.describe('Accessibility', () => {
    test('should have page title', async ({ page }) => {
      await page.goto('/static/index.html')
      
      await expect(page).toHaveTitle(/Acciones en cartera/)
    })

    test('should have proper heading structure', async ({ page }) => {
      await page.goto('/static/index.html')
      
      const h2 = page.locator('h2')
      await expect(h2).toBeVisible()
    })
  })
})
