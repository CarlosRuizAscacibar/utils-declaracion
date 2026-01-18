import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { mockFetchSuccess, mockFetchError } from '../mockFetch.js'
import { LoadFilesScreen } from '../../../static/main.js'

describe('LoadFilesScreen Integration Tests', () => {
  let loadFilesScreen
  let button
  let statusEl
  let outputEl

  beforeEach(() => {
    const loadFilesDiv = document.createElement('div')
    loadFilesDiv.setAttribute('data-screen', 'load_files_screen')
    loadFilesDiv.style.display = 'none'

    button = document.createElement('button')
    button.id = 'load-files-button'
    loadFilesDiv.appendChild(button)

    statusEl = document.createElement('div')
    statusEl.id = 'load-files-status'
    loadFilesDiv.appendChild(statusEl)

    outputEl = document.createElement('pre')
    outputEl.id = 'load-files-output'
    loadFilesDiv.appendChild(outputEl)

    document.body.appendChild(loadFilesDiv)

    vi.spyOn(window, 'alert').mockImplementation(() => {})

    loadFilesScreen = new LoadFilesScreen()
    loadFilesScreen.init()
  })

  afterEach(() => {
    const loadFilesDiv = document.querySelector('[data-screen="load_files_screen"]')
    if (loadFilesDiv) {
      loadFilesDiv.remove()
    }
    vi.restoreAllMocks()
  })

  describe('Initialization', () => {
    it('should have correct screen name', () => {
      expect(loadFilesScreen.screenName).toBe('load_files_screen')
    })

    it('should have button reference', () => {
      expect(loadFilesScreen.button).toBe(button)
    })

    it('should have status element reference', () => {
      expect(loadFilesScreen.status).toBe(statusEl)
    })

    it('should have output element reference', () => {
      expect(loadFilesScreen.output).toBe(outputEl)
    })

    it('should add event listener to button', () => {
      expect(loadFilesScreen.button.onclick).toBeDefined()
    })
  })

  describe('Load Files Functionality', () => {
    it('should call fetch with correct parameters on button click', async () => {
      mockFetchSuccess('/load_files', { message: 'Files loaded successfully', output: 'some output' })

      loadFilesScreen.button.click()

      expect(loadFilesScreen.button.disabled).toBe(true)
      expect(loadFilesScreen.button.textContent).toBe('Loading...')

      await new Promise(resolve => setTimeout(resolve, 0)) // Wait for async

      expect(global.fetch).toHaveBeenCalledWith('load_files', { method: 'POST' })
      expect(loadFilesScreen.button.disabled).toBe(false)
      expect(loadFilesScreen.button.textContent).toBe('Load All Files')
    })

    it('should show success alert and update UI on successful load', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      const mockOutput = 'Loading files...\nFiles loaded successfully\n'
      mockFetchSuccess('/load_files', { message: 'Files loaded successfully', output: mockOutput })

      loadFilesScreen.button.click()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('Files loaded successfully!')
      expect(loadFilesScreen.status.textContent).toBe('Files loaded successfully!')
      expect(loadFilesScreen.output.textContent).toBe(mockOutput)
      expect(loadFilesScreen.button.disabled).toBe(false)
      expect(loadFilesScreen.button.textContent).toBe('Load All Files')
      alertSpy.mockRestore()
    })

    it('should show error alert and update UI on failed load', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      const errorMessage = 'Script failed'
      mockFetchError('/load_files', 500, errorMessage)

      loadFilesScreen.button.click()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('Error loading files: ' + errorMessage)
      expect(loadFilesScreen.status.textContent).toBe('Error loading files.')
      expect(loadFilesScreen.output.textContent).toBe(errorMessage)
      expect(loadFilesScreen.button.disabled).toBe(false)
      expect(loadFilesScreen.button.textContent).toBe('Load All Files')
      alertSpy.mockRestore()
    })

    it('should show error alert on network error', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      const networkError = new Error('Network error')
      global.fetch.mockRejectedValueOnce(networkError)

      loadFilesScreen.button.click()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('Error: ' + networkError.message)
      expect(loadFilesScreen.status.textContent).toBe('Network error.')
      expect(loadFilesScreen.output.textContent).toBe(networkError.message)
      expect(loadFilesScreen.button.disabled).toBe(false)
      expect(loadFilesScreen.button.textContent).toBe('Load All Files')
      alertSpy.mockRestore()
    })

    it('should prevent multiple simultaneous requests', async () => {
      mockFetchSuccess('/load_files', { message: 'Files loaded successfully', output: '' })

      // Click button twice quickly
      loadFilesScreen.button.click()
      loadFilesScreen.button.click()

      expect(loadFilesScreen.button.disabled).toBe(true)

      await new Promise(resolve => setTimeout(resolve, 0))

      // Should only have been called once
      expect(global.fetch).toHaveBeenCalledTimes(1)
    })

    it('should clear output area when starting new request', async () => {
      // Set some initial output
      loadFilesScreen.output.textContent = 'previous output'

      mockFetchSuccess('/load_files', { message: 'Files loaded successfully', output: 'new output' })

      loadFilesScreen.button.click()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(loadFilesScreen.output.textContent).toBe('new output')
    })

    it('should update status text during loading', async () => {
      mockFetchSuccess('/load_files', { message: 'Files loaded successfully', output: '' })

      loadFilesScreen.button.click()

      expect(loadFilesScreen.status.textContent).toBe('Executing load_all_files.py...')

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(loadFilesScreen.status.textContent).toBe('Files loaded successfully!')
    })
  })
})