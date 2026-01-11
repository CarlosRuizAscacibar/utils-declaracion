import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { mockFetchSuccess, mockFetchError } from '../mockFetch.js'
import { DiferentesAcciones } from '../../../static/main.js'
import { diferentesAccionesResponse } from '../fixtures/mockData.js'

describe('DiferentesAcciones Integration Tests', () => {
  let diferentesAcciones
  let container

  beforeEach(() => {
    container = document.createElement('div')
    container.setAttribute('data-screen', 'diferentes_acciones')
    const list = document.createElement('ul')
    list.id = 'acciones-list'
    container.appendChild(list)
    document.body.appendChild(container)

    diferentesAcciones = new DiferentesAcciones()
  })

  afterEach(() => {
    const accionesDiv = document.querySelector('[data-screen="diferentes_acciones"]')
    if (accionesDiv) {
      accionesDiv.remove()
    }
  })

  describe('Initialization', () => {
    it('should initialize data array', () => {
      expect(diferentesAcciones.data).toEqual([])
    })

    it('should fetch acciones on init', async () => {
      mockFetchSuccess('/diferentes_acciones', diferentesAccionesResponse)

      await diferentesAcciones.init()

      expect(global.fetch).toHaveBeenCalledWith('diferentes_acciones')
      expect(diferentesAcciones.data).toEqual(diferentesAccionesResponse)
    })
  })

  describe('Data Rendering', () => {
    it('should render list items correctly', async () => {
      mockFetchSuccess('/diferentes_acciones', diferentesAccionesResponse)

      await diferentesAcciones.init()

      const listItems = container.querySelectorAll('li')
      expect(listItems.length).toBe(3)
    })

    it('should render first stock correctly', async () => {
      mockFetchSuccess('/diferentes_acciones', diferentesAccionesResponse)

      await diferentesAcciones.init()

      const firstItem = container.querySelector('li:first-child')
      const link = firstItem.querySelector('a')

      expect(link.textContent).toBe('Apple Inc.')
      expect(link.href).toContain('/static/cartera_isin.html')
      expect(link.href).toContain('isin=US5949724083')
      expect(link.href).toContain('selected_screen=cartera_accion')
    })

    it('should render all stocks correctly', async () => {
      mockFetchSuccess('/diferentes_acciones', diferentesAccionesResponse)

      await diferentesAcciones.init()

      const links = container.querySelectorAll('a')

      expect(links[0].textContent).toBe('Apple Inc.')
      expect(links[0].href).toContain('US5949724083')

      expect(links[1].textContent).toBe('Microsoft Corp.')
      expect(links[1].href).toContain('US5949181045')

      expect(links[2].textContent).toBe('Alphabet Inc.')
      expect(links[2].href).toContain('US02079K3059')
    })

    it('should clear previous content before rendering', async () => {
      const list = container.querySelector('#acciones-list')
      list.innerHTML = '<li>Old content</li>'

      mockFetchSuccess('/diferentes_acciones', diferentesAccionesResponse)

      await diferentesAcciones.init()

      expect(list.querySelector('li').textContent).not.toBe('Old content')
    })
  })

  describe('Error Handling', () => {
    it('should log error on HTTP error', async () => {
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
      mockFetchError('/diferentes_acciones', 500, 'Server Error')

      await diferentesAcciones.init()

      expect(consoleSpy).toHaveBeenCalledWith('Error fetching acciones:', expect.any(Error))
      expect(diferentesAcciones.data).toEqual([])

      consoleSpy.mockRestore()
    })

    it('should not throw error on network failure', async () => {
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      await diferentesAcciones.init()

      expect(consoleSpy).toHaveBeenCalledWith('Error fetching acciones:', expect.any(Error))

      consoleSpy.mockRestore()
    })

    it('should show error message on error', async () => {
      const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => {})
      mockFetchError('/diferentes_acciones', 404, 'Not Found')

      await diferentesAcciones.init()

      const listItems = container.querySelectorAll('li')
      expect(listItems.length).toBe(1)
      expect(listItems[0].textContent).toBe('Error loading stocks. Please check your connection and try again.')

      consoleSpy.mockRestore()
    })
  })

  describe('Empty Data', () => {
    it('should handle empty response', async () => {
      mockFetchSuccess('/diferentes_acciones', [])

      await diferentesAcciones.init()

      expect(diferentesAcciones.data).toEqual([])

      const listItems = container.querySelectorAll('li')
      expect(listItems.length).toBe(1)
      expect(listItems[0].textContent).toBe('No stocks found in your portfolio.')
    })
  })

  describe('Link Parameters', () => {
    it('should generate correct URL parameters for all stocks', async () => {
      mockFetchSuccess('/diferentes_acciones', diferentesAccionesResponse)

      await diferentesAcciones.init()

      const links = container.querySelectorAll('a')

      links.forEach(link => {
        expect(link.href).toContain('selected_screen=cartera_accion')
        expect(link.href).toContain('isin=')
      })
    })

    it('should use correct base URL', async () => {
      mockFetchSuccess('/diferentes_acciones', diferentesAccionesResponse)

      await diferentesAcciones.init()

      const links = container.querySelectorAll('a')

      links.forEach(link => {
        expect(link.href).toContain('/static/cartera_isin.html?')
      })
    })
  })
})
