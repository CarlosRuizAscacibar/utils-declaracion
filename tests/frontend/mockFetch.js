export function mockFetchSuccess(url, data) {
  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => data,
  })
}

export function mockFetchError(url, status = 500, message = 'Internal Server Error') {
  global.fetch.mockResolvedValueOnce({
    ok: false,
    status,
    json: async () => ({ error: message }),
  })
}

export function mockFetchNetworkError(url, error = new Error('Network error')) {
  global.fetch.mockRejectedValueOnce(error)
}

export function getMockCalls(url) {
  return global.fetch.mock.calls.filter(call => call[0].includes(url))
}

export function resetFetch() {
  global.fetch.mockClear()
}
