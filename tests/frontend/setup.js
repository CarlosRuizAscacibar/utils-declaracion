import { vi } from 'vitest'

global.fetch = vi.fn()

beforeEach(() => {
  vi.clearAllMocks()
  Object.defineProperty(window, 'location', {
    value: {
      search: '',
    },
    writable: true,
  })
})

afterEach(() => {
  document.body.innerHTML = ''
})
