import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { createScreenElement, mockURL } from '../domHelpers.js'
import { mockFetchSuccess, mockFetchError } from '../mockFetch.js'
import { YearReport } from '../../../static/main.js'
import { yearReportResponse, yearReportEmptyResponse } from '../fixtures/mockData.js'

describe('YearReport Integration Tests', () => {
  let yearReport
  let container

  beforeEach(() => {
    container = createScreenElement('year_report', `
      <p class="c-loading" style="display: none;">Loading…</p>
      <p class="c-error" style="display: none;"></p>

      <div class="year-content" style="display: none;">
        <section class="content">
          <h1 class="year-title"></h1>
          <table class="c-table" border="1">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Compra Fecha</th>
                <th>Precio Unitario Compra</th>
                <th>Venta Fecha</th>
                <th>Precio Unitario Venta</th>
                <th>Beneficio €</th>
              </tr>
            </thead>
            <tbody class="compra-ventas-tbody">
            </tbody>
          </table>

          <table class="c-table" border="1">
            <thead>
              <tr>
                <th>Concepto</th>
                <th>Fecha</th>
                <th>Importe €</th>
              </tr>
            </thead>
            <tbody class="dividendos-tbody">
            </tbody>
          </table>
        </section>
      </div>
    `)

    mockURL({ year: '2024' })
    yearReport = new YearReport()
  })

  afterEach(() => {
    document.querySelectorAll('[data-screen]').forEach(el => el.remove())
  })

  describe('Initialization', () => {
    it('should not init when no year in URL', () => {
      mockURL({})
      const screen = new YearReport()

      expect(() => screen.init()).not.toThrow()
    })

    it('should show loading state when fetching', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      const initPromise = yearReport.init()

      const loadingEl = container.querySelector('.c-loading')
      expect(loadingEl.style.display).toBe('block')

      await initPromise
      expect(loadingEl.style.display).toBe('none')
    })

    it('should hide loading state after fetch completes', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      await yearReport.init()

      const loadingEl = container.querySelector('.c-loading')
      expect(loadingEl.style.display).toBe('none')
    })
  })

  describe('Error Handling', () => {
    it('should show error message on HTTP error', async () => {
      mockFetchError('/report/year/2024', 404, 'Not Found')

      await yearReport.init()

      const errorEl = container.querySelector('.c-error')
      expect(errorEl.style.display).toBe('block')
      expect(errorEl.textContent).toBe('HTTP 404')
    })

    it('should hide content on error', async () => {
      mockFetchError('/report/year/2024', 500, 'Server Error')

      await yearReport.init()

      const contentEl = container.querySelector('.year-content')
      expect(contentEl.style.display).toBe('none')
    })

    it('should handle network error', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      await yearReport.init()

      const errorEl = container.querySelector('.c-error')
      expect(errorEl.style.display).toBe('block')
    })
  })

  describe('Data Rendering', () => {
    it('should render year title correctly', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      await yearReport.init()

      const yearEl = container.querySelector('.year-title')
      expect(yearEl.textContent).toBe('2024')
    })

    it('should show content after successful fetch', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      await yearReport.init()

      const contentEl = container.querySelector('.year-content')
      expect(contentEl.style.display).toBe('block')
    })
  })

  describe('Compra Ventas Table', () => {
    it('should render compra-ventas rows', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      await yearReport.init()

      const rows = container.querySelectorAll('.compra-ventas-tbody tr')
      expect(rows.length).toBe(3)

      const firstRow = rows[0]
      const cells = firstRow.querySelectorAll('td')
      expect(cells[0].textContent).toBe('Apple Inc.')
      expect(cells[1].textContent).toBe('2024-01-15')
      expect(cells[2].textContent).toBe('150')
      expect(cells[3].textContent).toBe('2024-02-01')
      expect(cells[4].textContent).toBe('180')
      expect(cells[5].textContent).toBe('750')
    })

    it('should render second compra-venta row', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      await yearReport.init()

      const rows = container.querySelectorAll('.compra-ventas-tbody tr')
      const secondRow = rows[1]
      const cells = secondRow.querySelectorAll('td')

      expect(cells[0].textContent).toBe('Microsoft Corp.')
      expect(cells[1].textContent).toBe('2024-03-01')
      expect(cells[2].textContent).toBe('300')
      expect(cells[3].textContent).toBe('2024-04-15')
      expect(cells[4].textContent).toBe('350')
      expect(cells[5].textContent).toBe('1250')
    })

    it('should render total row with benefit', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      await yearReport.init()

      const rows = container.querySelectorAll('.compra-ventas-tbody tr')
      const totalRow = rows[2]
      const cells = totalRow.querySelectorAll('td')

      expect(cells[0].textContent).toBe('TOTAL')
      expect(cells[5].textContent).toBe('5000')
    })
  })

  describe('Dividendos Table', () => {
    it('should render dividendos rows', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      await yearReport.init()

      const rows = container.querySelectorAll('.dividendos-tbody tr')
      expect(rows.length).toBe(4)

      const firstRow = rows[0]
      const cells = firstRow.querySelectorAll('td')
      expect(cells[0].textContent).toBe('Dividendo Apple Q1')
      expect(cells[1].textContent).toBe('2024-03-10')
      expect(cells[2].textContent).toBe('25')
    })

    it('should render all dividendos', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      await yearReport.init()

      const rows = container.querySelectorAll('.dividendos-tbody tr')
      
      expect(rows[0].querySelectorAll('td')[0].textContent).toBe('Dividendo Apple Q1')
      expect(rows[1].querySelectorAll('td')[0].textContent).toBe('Dividendo Apple Q2')
      expect(rows[2].querySelectorAll('td')[0].textContent).toBe('Dividendo Microsoft Q1')
    })

    it('should render total row with dividend benefit', async () => {
      mockFetchSuccess('/report/year/2024', yearReportResponse)

      await yearReport.init()

      const rows = container.querySelectorAll('.dividendos-tbody tr')
      const totalRow = rows[3]
      const cells = totalRow.querySelectorAll('td')

      expect(cells[0].textContent).toBe('TOTAL')
      expect(cells[2].textContent).toBe('1000')
    })
  })

  describe('Empty Data', () => {
    it('should handle empty data response', async () => {
      mockFetchSuccess('/report/year/2025', yearReportEmptyResponse)

      await yearReport.init()

      const compraVentasRows = container.querySelectorAll('.compra-ventas-tbody tr')
      expect(compraVentasRows.length).toBe(1)

      const dividendosRows = container.querySelectorAll('.dividendos-tbody tr')
      expect(dividendosRows.length).toBe(1)
    })

    it('should render total rows with zero values', async () => {
      mockFetchSuccess('/report/year/2025', yearReportEmptyResponse)

      await yearReport.init()

      const compraVentasRows = container.querySelectorAll('.compra-ventas-tbody tr')
      const totalRow = compraVentasRows[0]
      const cells = totalRow.querySelectorAll('td')

      expect(cells[0].textContent).toBe('TOTAL')
      expect(cells[5].textContent).toBe('0')

      const dividendosRows = container.querySelectorAll('.dividendos-tbody tr')
      const dividendosTotalRow = dividendosRows[0]
      const dividendosCells = dividendosTotalRow.querySelectorAll('td')

      expect(dividendosCells[0].textContent).toBe('TOTAL')
      expect(dividendosCells[2].textContent).toBe('0')
    })
  })
})
