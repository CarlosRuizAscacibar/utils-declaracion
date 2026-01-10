import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { createScreenElement, mockURL } from '../domHelpers.js'
import { mockFetchSuccess, mockFetchError } from '../mockFetch.js'
import { CarteraScreen } from '../../../static/main.js'
import { carteraResponse, carteraEmptyResponse } from '../fixtures/mockData.js'

describe('CarteraScreen Integration Tests', () => {
  let carteraScreen
  let container

  beforeEach(() => {
    container = createScreenElement('cartera_accion', `
      <p class="c-loading" style="display: none;">Loading cartera…</p>
      <p class="c-error" style="display: none;"></p>
      <div class="cartera-content" style="display: none;">
        <div>
          <div>
            <h2 class="accion-nombre"></h2>
            <p class="muted">
              ISIN: <span class="accion-isin"></span>
            </p>
          </div>
          <section>
            <h3>Operaciones</h3>
            <table class="c-table">
              <thead>
                <tr>
                  <th>Fecha</th>
                  <th>Tipo</th>
                  <th>Cantidad</th>
                  <th>divisa</th>
                  <th>Precio</th>
                  <th>Importe</th>
                  <th>Broker</th>
                  <th>Dias Ultima Venta</th>
                  <th>Restantes</th>
                </tr>
              </thead>
              <tbody class="operaciones-tbody">
              </tbody>
            </table>
            <p>
              Acciones actual <b class="acciones-actual"></b> Valor: <b class="valor-actual"></b>
            </p>
          </section>
          <section>
            <h3>Compras y Ventas Asociadas</h3>
            <div class="compra-ventas-container"></div>
          </section>
          <section>
            <h3>Dividendos</h3>
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
      </div>
    `)

    mockURL({ isin: 'US5949724083' })
    carteraScreen = new CarteraScreen()
  })

  afterEach(() => {
    document.querySelectorAll('[data-screen]').forEach(el => el.remove())
  })

  describe('Initialization', () => {
    it('should not init when no ISIN in URL', () => {
      mockURL({})
      const screen = new CarteraScreen()
      
      expect(() => screen.init()).not.toThrow()
    })

    it('should show loading state when fetching', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      const initPromise = carteraScreen.init()
      
      const loadingEl = container.querySelector('.c-loading')
      expect(loadingEl.style.display).toBe('block')

      await initPromise
      expect(loadingEl.style.display).toBe('none')
    })

    it('should hide loading state after fetch completes', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const loadingEl = container.querySelector('.c-loading')
      expect(loadingEl.style.display).toBe('none')
    })
  })

  describe('Error Handling', () => {
    it('should show error message on HTTP error', async () => {
      mockFetchError('/cartera/US5949724083', 404, 'Not Found')

      await carteraScreen.init()

      const errorEl = container.querySelector('.c-error')
      expect(errorEl.style.display).toBe('block')
      expect(errorEl.textContent).toBe('HTTP 404')
    })

    it('should hide content on error', async () => {
      mockFetchError('/cartera/US5949724083', 500, 'Server Error')

      await carteraScreen.init()

      const contentEl = container.querySelector('.cartera-content')
      expect(contentEl.style.display).toBe('none')
    })

    it('should handle network error', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      await carteraScreen.init()

      const errorEl = container.querySelector('.c-error')
      expect(errorEl.style.display).toBe('block')
    })
  })

  describe('Data Rendering', () => {
    it('should render stock name correctly', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const nombreEl = container.querySelector('.accion-nombre')
      expect(nombreEl.textContent).toBe('Apple Inc.')
    })

    it('should render ISIN correctly', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const isinEl = container.querySelector('.accion-isin')
      expect(isinEl.textContent).toBe('US5949724083')
    })

    it('should render acciones actual and valor actual', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const accionesEl = container.querySelector('.acciones-actual')
      const valorEl = container.querySelector('.valor-actual')
      
      expect(accionesEl.textContent).toBe('100')
      expect(valorEl.textContent).toBe('15000.5')
    })

    it('should show content after successful fetch', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const contentEl = container.querySelector('.cartera-content')
      expect(contentEl.style.display).toBe('block')
    })
  })

  describe('Operaciones Table', () => {
    it('should render compra operation correctly', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const rows = container.querySelectorAll('.operaciones-tbody tr')
      expect(rows.length).toBe(4)

      const firstRow = rows[0]
      const cells = firstRow.querySelectorAll('td')
      expect(cells[0].textContent).toBe('2024-01-15')
      expect(cells[1].textContent).toBe('Compra')
      expect(cells[2].textContent).toBe('50')
      expect(cells[3].textContent).toBe('EUR')
      expect(cells[4].textContent).toBe('150')
      expect(cells[5].textContent).toBe('7500')
      expect(cells[6].textContent).toBe('Degiro')
      expect(cells[7].textContent).toBe('30')
      expect(cells[8].textContent).toBe('50')
    })

    it('should render venta operation correctly', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const rows = container.querySelectorAll('.operaciones-tbody tr')
      const secondRow = rows[1]
      const cells = secondRow.querySelectorAll('td')
      
      expect(cells[1].textContent).toBe('Venta')
      expect(cells[2].textContent).toBe('25')
    })

    it('should render dividendo operation correctly', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const rows = container.querySelectorAll('.operaciones-tbody tr')
      const thirdRow = rows[2]
      const cells = thirdRow.querySelectorAll('td')
      
      expect(cells[1].textContent).toBe('Dividendo')
      expect(cells[2].textContent).toBe('0')
      expect(cells[3].textContent).toBe('USD')
    })

    it('should render split operation with colspan', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const rows = container.querySelectorAll('.operaciones-tbody tr')
      const fourthRow = rows[3]
      const cells = fourthRow.querySelectorAll('td')
      
      expect(cells[0].textContent).toBe('2024-04-01')
      expect(cells[1].textContent).toBe('Split')
      expect(cells[2].textContent).toContain('25')
      expect(cells[2].textContent).toContain('50')
    })
  })

  describe('Compra Ventas Report', () => {
    it('should render compra-ventas cards', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const cards = container.querySelectorAll('.compra-ventas-container .c-card')
      expect(cards.length).toBe(1)

      const cardContent = cards[0].textContent
      expect(cardContent).toContain('C:')
      expect(cardContent).toContain('2024-01-15')
      expect(cardContent).toContain('150')
      expect(cardContent).toContain('V:')
      expect(cardContent).toContain('2024-02-01')
      expect(cardContent).toContain('180')
      expect(cardContent).toContain('750')
    })
  })

  describe('Dividendos Table', () => {
    it('should render dividendos rows', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const rows = container.querySelectorAll('.dividendos-tbody tr')
      expect(rows.length).toBe(2)

      const firstRow = rows[0]
      const cells = firstRow.querySelectorAll('td')
      expect(cells[0].textContent).toBe('Dividendo Q1 2024')
      expect(cells[1].textContent).toBe('2024-03-10')
      expect(cells[2].textContent).toBe('25')
    })

    it('should render total row', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraResponse)

      await carteraScreen.init()

      const rows = container.querySelectorAll('.dividendos-tbody tr')
      const totalRow = rows[1]
      const cells = totalRow.querySelectorAll('td')
      
      expect(cells[0].textContent).toBe('TOTAL')
      expect(cells[2].textContent).toBe('25')
    })
  })

  describe('Empty Data', () => {
    it('should handle empty data response', async () => {
      mockFetchSuccess('/cartera/US5949724083', carteraEmptyResponse)

      await carteraScreen.init()

      const rows = container.querySelectorAll('.operaciones-tbody tr')
      expect(rows.length).toBe(0)

      const cards = container.querySelectorAll('.compra-ventas-container .c-card')
      expect(cards.length).toBe(0)
    })
  })
})
