import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { mockFetchSuccess, mockFetchError } from '../mockFetch.js'
import { Backup } from '../../../static/main.js'

describe('Backup Integration Tests', () => {
  let backup
  let button
  let lastBackupEl

  beforeEach(() => {
    const backupDiv = document.createElement('div')
    backupDiv.style.display = 'none'
    button = document.createElement('button')
    button.id = 'backup-button'
    backupDiv.appendChild(button)

    lastBackupEl = document.createElement('p')
    lastBackupEl.id = 'last-backup-info'
    backupDiv.appendChild(lastBackupEl)

    document.body.appendChild(backupDiv)

    vi.spyOn(window, 'alert').mockImplementation(() => {})

    backup = new Backup()
    backup.init()
  })

  afterEach(() => {
    const backupDiv = document.querySelector('#backup-button')?.parentElement
    if (backupDiv) {
      backupDiv.remove()
    }
    vi.restoreAllMocks()
  })

  describe('Initialization', () => {
    it('should have button reference', () => {
      expect(backup.button).toBe(button)
    })

    it('should add event listener to button', () => {
      expect(backup.button.onclick).toBeDefined()
    })
  })

  describe('Backup Functionality', () => {
    it('should call fetch with correct parameters on button click', async () => {
      mockFetchSuccess('/backup', {})

      backup.button.click()

      await new Promise(resolve => setTimeout(resolve, 0)) // Wait for async

      expect(global.fetch).toHaveBeenCalledWith('/backup', { method: 'POST' })
    })

    it('should show success alert on successful backup', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      mockFetchSuccess('/backup', {})

      backup.button.click()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('Backup completed successfully!')
      alertSpy.mockRestore()
    })

    it('should show error alert on failed backup', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      mockFetchError('/backup', 500, 'Server Error')

      backup.button.click()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('Backup failed: 500')
      alertSpy.mockRestore()
    })

    it('should show error alert on network error', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      backup.button.click()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('Backup error: Network error')
      alertSpy.mockRestore()
    })

    it('should display last backup info on init', async () => {
      const mockLastBackup = { last_backup: '2023-10-15T14:30:00' }
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockLastBackup
      })

      backup.init()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(backup.lastBackupEl.textContent).toContain('Last backup:')
    })

    it('should display no backups yet when no last backup', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ last_backup: null })
      })

      backup.init()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(backup.lastBackupEl.textContent).toBe('No backups yet')
    })

    it('should update last backup display after successful backup', async () => {
      const alertSpy = vi.spyOn(window, 'alert').mockImplementation(() => {})
      mockFetchSuccess('/backup', {})
      const mockLastBackup = { last_backup: '2023-10-15T14:30:00' }
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockLastBackup
      })

      backup.button.click()

      await new Promise(resolve => setTimeout(resolve, 0))

      expect(alertSpy).toHaveBeenCalledWith('Backup completed successfully!')
      expect(backup.lastBackupEl.textContent).toContain('Last backup:')
      alertSpy.mockRestore()
    })
  })
})