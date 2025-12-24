function application() {
    return {
        screen: 'no_screen',

        init() {
            this.syncFromUrl()
            window.addEventListener('popstate', () => this.syncFromUrl())
        },

        syncFromUrl() {
            this.screen =
                new URLSearchParams(location.search)
                    .get('selected_screen') ?? 'no_screen'
        }
    }
}

function carteraScreen() {
  return {
    isin: new URLSearchParams(location.search)
                    .get('isin') ,
    data: null,
    loading: false,
    error: null,

    async init() {
      this.loading = true
      try {
        const res = await fetch(`/cartera/${this.isin}`)
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`)
        }
        this.data = await res.json()
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    }
  }
}

function yearReport() {
  return {
    year: new URLSearchParams(location.search)
                    .get('year') ,
    data: null,
    loading: false,
    error: null,

    async init() {
      this.loading = true
      try {
        const res = await fetch(`/report/year/${this.year}`)
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}`)
        }
        this.data = await res.json()
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    }
  }
}

function diferentesAcciones(){
  return {
    data: [],
    async init(){
      const res = await fetch(`/diferentes_acciones`)
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`)
      }
      this.data = await res.json()
    }

  }
}