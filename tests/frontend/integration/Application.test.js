import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { createScreenElement, mockURL, triggerPopState } from '../domHelpers.js'
import { Application } from '../../../static/main.js'

describe('Application Integration Tests', () => {
  let app

  beforeEach(() => {
    app = new Application()
  })

  afterEach(() => {
    document.querySelectorAll('[data-screen]').forEach(el => el.remove())
  })

  describe('Screen Registration', () => {
    it('should register a screen', () => {
      const mockScreen = { init: vi.fn() }
      app.registerScreen('test_screen', mockScreen)

      expect(app.screens.has('test_screen')).toBe(true)
      expect(app.screens.get('test_screen')).toBe(mockScreen)
    })

    it('should replace existing screen when registering with same name', () => {
      const mockScreen1 = { init: vi.fn() }
      const mockScreen2 = { init: vi.fn() }

      app.registerScreen('test_screen', mockScreen1)
      app.registerScreen('test_screen', mockScreen2)

      expect(app.screens.get('test_screen')).toBe(mockScreen2)
    })
  })

  describe('Screen Display', () => {
    it('should hide all screens by default', () => {
      createScreenElement('home')
      createScreenElement('cartera_accion')

      const screens = document.querySelectorAll('[data-screen]')
      expect(screens).toHaveLength(2)

      screens.forEach(screen => {
        expect(screen.style.display).toBe('none')
      })
    })

    it('should show registered screen when init() is called', () => {
      const mockScreen = { init: vi.fn() }
      app.registerScreen('test_screen', mockScreen)

      mockURL({ selected_screen: 'test_screen' })
      app.init()

      expect(mockScreen.init).toHaveBeenCalled()
    })

    it('should not call init for unregistered screens', () => {
      const mockScreen = { init: vi.fn() }
      app.registerScreen('test_screen', mockScreen)

      mockURL({ selected_screen: 'unregistered_screen' })
      app.init()

      expect(mockScreen.init).not.toHaveBeenCalled()
    })

    it('should handle no_screen as default', () => {
      mockURL({})
      app.init()

      expect(app.currentScreen).toBe('no_screen')
    })
  })

  describe('URL Synchronization', () => {
    it('should sync screen from URL on init', () => {
      mockURL({ selected_screen: 'cartera_accion' })
      app.init()

      expect(app.currentScreen).toBe('cartera_accion')
    })

    it('should use no_screen when no selected_screen parameter', () => {
      mockURL({})
      app.init()

      expect(app.currentScreen).toBe('no_screen')
    })

    it('should update screen on popstate event', () => {
      const mockScreen = { init: vi.fn() }
      app.registerScreen('test_screen', mockScreen)

      app.init()

      mockURL({ selected_screen: 'test_screen' })
      triggerPopState()

      expect(app.currentScreen).toBe('test_screen')
      expect(mockScreen.init).toHaveBeenCalled()
    })

    it('should handle popstate event without registered screen', () => {
      const mockScreen = { init: vi.fn() }
      app.registerScreen('test_screen', mockScreen)

      app.init()

      mockURL({ selected_screen: 'unregistered' })
      triggerPopState()

      expect(app.currentScreen).toBe('unregistered')
      expect(mockScreen.init).not.toHaveBeenCalled()
    })
  })

  describe('showScreen', () => {
    it('should hide all screens when showing a new screen', () => {
      const screen1 = createScreenElement('screen1')
      const screen2 = createScreenElement('screen2')

      screen1.style.display = 'block'
      screen2.style.display = 'block'

      const mockScreen = { init: vi.fn() }
      app.registerScreen('screen1', mockScreen)

      app.showScreen('screen1')

      expect(screen1.style.display).toBe('none')
      expect(screen2.style.display).toBe('none')
    })

    it('should call init() on the screen being shown', () => {
      const mockScreen = { init: vi.fn() }
      app.registerScreen('test_screen', mockScreen)

      app.showScreen('test_screen')

      expect(mockScreen.init).toHaveBeenCalledTimes(1)
    })

    it('should not throw error when showing non-existent screen', () => {
      expect(() => {
        app.showScreen('non_existent_screen')
      }).not.toThrow()
    })
  })

  describe('State Management', () => {
    it('should track current screen correctly', () => {
      mockURL({ selected_screen: 'year_report' })
      app.init()

      expect(app.currentScreen).toBe('year_report')
    })

    it('should update current screen on URL change', () => {
      mockURL({ selected_screen: 'screen1' })
      app.init()

      expect(app.currentScreen).toBe('screen1')

      mockURL({ selected_screen: 'screen2' })
      triggerPopState()

      expect(app.currentScreen).toBe('screen2')
    })
  })
})
