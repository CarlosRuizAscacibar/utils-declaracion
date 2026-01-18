import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { mockFetchSuccess, mockFetchError } from '../mockFetch.js'
import { InvestorDataScreen } from '../../../static/main.js'

describe('InvestorDataScreen Integration Tests', () => {
  let investorDataScreen
  let form
  let button
  let statusEl
  let outputEl
  let usernameInput
  let passwordInput

  beforeEach(() => {
    const investorDataDiv = document.createElement('div')
    investorDataDiv.setAttribute('data-screen', 'investor_data_screen')
    investorDataDiv.style.display = 'none'

    form = document.createElement('form')
    form.id = 'investor-data-form'
    investorDataDiv.appendChild(form)

    usernameInput = document.createElement('input')
    usernameInput.type = 'text'
    usernameInput.name = 'username'
    form.appendChild(usernameInput)

    passwordInput = document.createElement('input')
    passwordInput.type = 'password'
    passwordInput.name = 'password'
    form.appendChild(passwordInput)

    button = document.createElement('button')
    button.type = 'submit'
    button.id = 'get-investor-data-button'
    form.appendChild(button)

    statusEl = document.createElement('div')
    statusEl.id = 'investor-data-status'
    investorDataDiv.appendChild(statusEl)

    outputEl = document.createElement('pre')
    outputEl.id = 'investor-data-output'
    investorDataDiv.appendChild(outputEl)

    document.body.appendChild(investorDataDiv)

    vi.spyOn(window, 'alert').mockImplementation(() => {})

    investorDataScreen = new InvestorDataScreen()
    investorDataScreen.init()
  })

  afterEach(() => {
    const investorDataDiv = document.querySelector('[data-screen="investor_data_screen"]')
    if (investorDataDiv) {
      investorDataDiv.remove()
    }
    vi.restoreAllMocks()
  })

  describe('Initialization', () => {
    it('should have correct screen name', () => {
      expect(investorDataScreen.screenName).toBe('investor_data_screen')
    })

    it('should have form reference', () => {
      expect(investorDataScreen.form).toBe(form)
    })

    it('should have button reference', () => {
      expect(investorDataScreen.button).toBe(button)
    })

    it('should have status element reference', () => {
      expect(investorDataScreen.status).toBe(statusEl)
    })

    it('should have output element reference', () => {
      expect(investorDataScreen.output).toBe(outputEl)
    })

    it('should add event listener to form', () => {
      expect(investorDataScreen.form.onsubmit).toBeDefined()
    })
  })

  describe('Form Submission', () => {
    it('should prevent default form submission', async () => {
      const preventDefaultSpy = vi.fn()
      const mockEvent = { preventDefault: preventDefaultSpy }

      usernameInput.value = 'testuser'
      passwordInput.value = 'testpass'

      mockFetchSuccess('/get_investor_data', { message: 'Investor data retrieved successfully', output: 'some output' })

      investorDataScreen.handleSubmit(mockEvent)

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(preventDefaultSpy).toHaveBeenCalled()
    })

    it('should show alert when username is missing', () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})

      usernameInput.value = ''
      passwordInput.value = 'testpass'

      form.dispatchEvent(new Event('submit'))

      expect(alertSpy).toHaveBeenCalledWith('Please fill in both username and password')
      alertSpy.mockRestore()
    })

    it('should show alert when password is missing', () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})

      usernameInput.value = 'testuser'
      passwordInput.value = ''

      form.dispatchEvent(new Event('submit'))

      expect(alertSpy).toHaveBeenCalledWith('Please fill in both username and password')
      alertSpy.mockRestore()
    })

    it('should call fetch with correct parameters on valid form submission', async () => {
      usernameInput.value = 'testuser'
      passwordInput.value = 'testpass'

      mockFetchSuccess('/get_investor_data', { message: 'Investor data retrieved successfully', output: 'some output' })

      form.dispatchEvent(new Event('submit'))

      expect(investorDataScreen.button.disabled).toBe(true)
      expect(investorDataScreen.button.textContent).toBe('Getting data...')

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(global.fetch).toHaveBeenCalledWith('get_investor_data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'testuser', password: 'testpass' })
      })
      expect(investorDataScreen.button.disabled).toBe(false)
      expect(investorDataScreen.button.textContent).toBe('Get Investor Data')
    })

    it('should show success alert and update UI on successful data retrieval', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      const mockOutput = 'Orders: success\nMovements: success'
      mockFetchSuccess('/get_investor_data', { message: 'Investor data retrieved successfully', output: mockOutput })

      usernameInput.value = 'testuser'
      passwordInput.value = 'testpass'

      form.dispatchEvent(new Event('submit'))

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('MyInvestor data retrieved successfully!')
      expect(investorDataScreen.status.textContent).toBe('MyInvestor data retrieved successfully!')
      expect(investorDataScreen.output.textContent).toBe(mockOutput)
      expect(investorDataScreen.button.disabled).toBe(false)
      expect(investorDataScreen.button.textContent).toBe('Get Investor Data')
      alertSpy.mockRestore()
    })

    it('should show error alert and update UI on failed data retrieval', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      const errorMessage = 'Authentication failed'
      mockFetchError('/get_investor_data', 500, errorMessage)

      usernameInput.value = 'testuser'
      passwordInput.value = 'testpass'

      form.dispatchEvent(new Event('submit'))

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('Error retrieving MyInvestor data: ' + errorMessage)
      expect(investorDataScreen.status.textContent).toBe('Error retrieving MyInvestor data.')
      expect(investorDataScreen.output.textContent).toBe(errorMessage)
      expect(investorDataScreen.button.disabled).toBe(false)
      expect(investorDataScreen.button.textContent).toBe('Get Investor Data')
      alertSpy.mockRestore()
    })

    it('should show error alert on network error', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      const networkError = new Error('Network error')
      global.fetch.mockRejectedValueOnce(networkError)

      usernameInput.value = 'testuser'
      passwordInput.value = 'testpass'

      form.dispatchEvent(new Event('submit'))

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('Error: ' + networkError.message)
      expect(investorDataScreen.status.textContent).toBe('Network error.')
      expect(investorDataScreen.output.textContent).toBe(networkError.message)
      expect(investorDataScreen.button.disabled).toBe(false)
      expect(investorDataScreen.button.textContent).toBe('Get Investor Data')
      alertSpy.mockRestore()
    })

    it('should prevent multiple simultaneous requests', async () => {
      usernameInput.value = 'testuser'
      passwordInput.value = 'testpass'

      mockFetchSuccess('/get_investor_data', { message: 'Investor data retrieved successfully', output: '' })

      // Submit form twice quickly
      form.dispatchEvent(new Event('submit'))
      form.dispatchEvent(new Event('submit'))

      expect(investorDataScreen.button.disabled).toBe(true)

      await new Promise(resolve => setTimeout(resolve, 0))

      // Should only have been called once
      expect(global.fetch).toHaveBeenCalledTimes(1)
    })

    it('should clear output area when starting new request', async () => {
      // Set some initial output
      investorDataScreen.output.textContent = 'previous output'

      usernameInput.value = 'testuser'
      passwordInput.value = 'testpass'

      mockFetchSuccess('/get_investor_data', { message: 'Investor data retrieved successfully', output: 'new output' })

      form.dispatchEvent(new Event('submit'))

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(investorDataScreen.output.textContent).toBe('new output')
    })

    it('should update status text during loading', async () => {
      usernameInput.value = 'testuser'
      passwordInput.value = 'testpass'

      mockFetchSuccess('/get_investor_data', { message: 'MyInvestor data retrieved successfully', output: '' })

      form.dispatchEvent(new Event('submit'))

      expect(investorDataScreen.status.textContent).toBe('Retrieving MyInvestor data...')

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(investorDataScreen.status.textContent).toBe('MyInvestor data retrieved successfully!')
    })
  })
})