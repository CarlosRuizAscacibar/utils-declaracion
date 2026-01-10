export function createScreenElement(screenName, innerHTML = '') {
  const div = document.createElement('div')
  div.dataset.screen = screenName
  div.style.display = 'none'
  div.innerHTML = innerHTML
  document.body.appendChild(div)
  return div
}

export function clearScreens() {
  document.querySelectorAll('[data-screen]').forEach(el => {
    el.remove()
  })
}

export function getScreenElement(screenName) {
  return document.querySelector(`[data-screen="${screenName}"]`)
}

export function createHTMLFromTemplate(html) {
  const template = document.createElement('template')
  template.innerHTML = html.trim()
  return template.content.firstChild
}

export function waitForElement(selector, timeout = 5000) {
  return new Promise((resolve, reject) => {
    const element = document.querySelector(selector)
    if (element) {
      return resolve(element)
    }

    const observer = new MutationObserver(() => {
      const element = document.querySelector(selector)
      if (element) {
        observer.disconnect()
        resolve(element)
      }
    })

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    })

    setTimeout(() => {
      observer.disconnect()
      reject(new Error(`Element ${selector} not found within ${timeout}ms`))
    }, timeout)
  })
}

export function mockURL(searchParams = {}) {
  const url = new URL('http://localhost/static/cartera_isin.html')
  Object.entries(searchParams).forEach(([key, value]) => {
    url.searchParams.set(key, value)
  })
  
  Object.defineProperty(window, 'location', {
    value: {
      search: url.search,
    },
    writable: true,
  })

  return url
}

export function triggerPopState(state = null) {
  const popStateEvent = new PopStateEvent('popstate', { state })
  window.dispatchEvent(popStateEvent)
}

export function mockLocalStorage() {
  const store = {}

  return {
    getItem: (key) => store[key],
    setItem: (key, value) => {
      store[key] = value.toString()
    },
    removeItem: (key) => {
      delete store[key]
    },
    clear: () => {
      Object.keys(store).forEach(key => delete store[key])
    },
  }
}
