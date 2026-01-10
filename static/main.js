export class Application {
    constructor() {
        this.screens = new Map()
        this.currentScreen = 'no_screen'
    }

    init() {
        this.syncFromUrl()
        window.addEventListener('popstate', () => this.syncFromUrl())
    }

    syncFromUrl() {
        this.currentScreen = new URLSearchParams(location.search).get('selected_screen') ?? 'no_screen'
        this.showScreen(this.currentScreen)
    }

    registerScreen(name, component) {
        this.screens.set(name, component)
    }

    showScreen(screenName) {
        document.querySelectorAll('[data-screen]').forEach(el => {
            el.style.display = 'none'
        })

        const screen = this.screens.get(screenName)
        if (screen) {
            screen.init()
        }
    }
}

export class CarteraScreen {
    constructor() {
        this.isin = new URLSearchParams(location.search).get('isin')
        this.data = null
        this.loading = false
        this.error = null
        this.container = document.querySelector('[data-screen="cartera_accion"]')
    }

    async init() {
        if (!this.isin) return
        
        this.container.style.display = 'block'
        this.setLoading(true)
        this.clearError()

        try {
            const res = await fetch(`/cartera/${this.isin}`)
            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`)
            }
            this.data = await res.json()
            this.render()
        } catch (e) {
            this.error = e.message
            this.renderError()
        } finally {
            this.setLoading(false)
        }
    }

    setLoading(loading) {
        this.loading = loading
        const loadingEl = this.container.querySelector('.c-loading')
        if (loadingEl) {
            loadingEl.style.display = loading ? 'block' : 'none'
        }
    }

    setError(error) {
        this.error = error
        const errorEl = this.container.querySelector('.c-error')
        if (errorEl) {
            errorEl.textContent = error
            errorEl.style.display = 'block'
        }
    }

    clearError() {
        const errorEl = this.container.querySelector('.c-error')
        if (errorEl) {
            errorEl.textContent = ''
            errorEl.style.display = 'none'
        }
    }

    renderError() {
        this.setError(this.error)
        const contentEl = this.container.querySelector('.cartera-content')
        if (contentEl) {
            contentEl.style.display = 'none'
        }
    }

    render() {
        this.clearError()
        const contentEl = this.container.querySelector('.cartera-content')
        if (contentEl) {
            contentEl.style.display = 'block'
        }

        const titleEl = this.container.querySelector('.accion-nombre')
        if (titleEl && this.data.operaciones?.[0]) {
            titleEl.textContent = this.data.operaciones[0].nombre
        }

        const isinEl = this.container.querySelector('.accion-isin')
        if (isinEl) {
            isinEl.textContent = this.data.isin
        }

        const accionesEl = this.container.querySelector('.acciones-actual')
        if (accionesEl) {
            accionesEl.textContent = this.data.acciones_actual
        }

        const valorEl = this.container.querySelector('.valor-actual')
        if (valorEl) {
            valorEl.textContent = this.data.valor_actual
        }

        this.renderOperaciones()
        this.renderCompraVentas()
        this.renderDividendos()
    }

    renderOperaciones() {
        const tbody = this.container.querySelector('.operaciones-tbody')
        if (!tbody) return

        tbody.innerHTML = ''

        const tipoLabels = {
            1: 'Compra',
            2: 'Venta',
            3: 'Dividendo',
            4: 'Split'
        }

        this.data.operaciones.forEach(op => {
            const tr = document.createElement('tr')

            const tipo = tipoLabels[op.tipo] ?? 'Desconocido'

            if (op.tipo === 4) {
                tr.innerHTML = `
                    <td>${op.fecha}</td>
                    <td>${tipo}</td>
                    <td colspan="4"><b>${op.numOriginal}</b> -> <b>${op.numDestino}</b></td>
                    <td></td>
                    <td></td>
                    <td></td>
                `
            } else {
                tr.innerHTML = `
                    <td>${op.fecha}</td>
                    <td>${tipo}</td>
                    <td style="text-align: center;">${op.cantidad}</td>
                    <td>${op.divisa}</td>
                    <td>${op.precio_unitario}</td>
                    <td>${op.importe_neto}</td>
                    <td>${op.broker}</td>
                    <td style="text-align: right;">${op.dias_ultima_venta}</td>
                    <td style="text-align: center;">${op.restantes}</td>
                `
            }

            tbody.appendChild(tr)
        })
    }

    renderCompraVentas() {
        const container = this.container.querySelector('.compra-ventas-container')
        if (!container) return

        container.innerHTML = ''

        this.data.compra_ventas_report.forEach(cv => {
            const card = document.createElement('div')
            card.className = 'c-card'
            card.innerHTML = `
                <p>
                    <strong>C:</strong>
                    <span>${cv.fecha_compra}</span> —
                    <span>${cv.precio_unitario_compra}</span>
                    &nbsp;
                    <strong>V:</strong>
                    <span>${cv.fecha_venta}</span> —
                    <span>${cv.precio_unitario_venta}</span>
                    <strong>Beneficio €:</strong>
                    <span>${cv.ganancia_perdida_eur}</span>
                </p>
            `
            container.appendChild(card)
        })
    }

    renderDividendos() {
        const tbody = this.container.querySelector('.dividendos-tbody')
        if (!tbody) return

        tbody.innerHTML = ''

        this.data.dividendos.forEach(cv => {
            const tr = document.createElement('tr')
            tr.innerHTML = `
                <td>${cv.concepto}</td>
                <td>${cv.fecha_valor}</td>
                <td>${cv.importe}</td>
            `
            tbody.appendChild(tr)
        })

        const totalRow = document.createElement('tr')
        totalRow.innerHTML = `
            <td><b>TOTAL</b></td>
            <td></td>
            <td><b>${this.data.beneficio_dividendos}</b></td>
        `
        tbody.appendChild(totalRow)
    }
}

export class YearReport {
    constructor() {
        this.year = new URLSearchParams(location.search).get('year')
        this.data = null
        this.loading = false
        this.error = null
        this.container = document.querySelector('[data-screen="year_report"]')
    }

    async init() {
        if (!this.year) return

        this.container.style.display = 'block'
        this.setLoading(true)
        this.clearError()

        try {
            const res = await fetch(`/report/year/${this.year}`)
            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`)
            }
            this.data = await res.json()
            this.render()
        } catch (e) {
            this.error = e.message
            this.renderError()
        } finally {
            this.setLoading(false)
        }
    }

    setLoading(loading) {
        this.loading = loading
        const loadingEl = this.container.querySelector('.c-loading')
        if (loadingEl) {
            loadingEl.style.display = loading ? 'block' : 'none'
        }
    }

    setError(error) {
        this.error = error
        const errorEl = this.container.querySelector('.c-error')
        if (errorEl) {
            errorEl.textContent = error
            errorEl.style.display = 'block'
        }
    }

    clearError() {
        const errorEl = this.container.querySelector('.c-error')
        if (errorEl) {
            errorEl.textContent = ''
            errorEl.style.display = 'none'
        }
    }

    renderError() {
        this.setError(this.error)
        const contentEl = this.container.querySelector('.year-content')
        if (contentEl) {
            contentEl.style.display = 'none'
        }
    }

    render() {
        this.clearError()
        const contentEl = this.container.querySelector('.year-content')
        if (contentEl) {
            contentEl.style.display = 'block'
        }

        const yearEl = this.container.querySelector('.year-title')
        if (yearEl) {
            yearEl.textContent = this.data.year
        }

        this.renderCompraVentas()
        this.renderDividendos()
    }

    renderCompraVentas() {
        const tbody = this.container.querySelector('.compra-ventas-tbody')
        if (!tbody) return

        tbody.innerHTML = ''

        this.data.compra_ventas_report.forEach(cv => {
            const tr = document.createElement('tr')
            tr.innerHTML = `
                <td>${cv.nombre}</td>
                <td>${cv.fecha_compra}</td>
                <td>${cv.precio_unitario_compra}</td>
                <td>${cv.fecha_venta}</td>
                <td>${cv.precio_unitario_venta}</td>
                <td>${cv.ganancia_perdida_eur}</td>
            `
            tbody.appendChild(tr)
        })

        const totalRow = document.createElement('tr')
        totalRow.innerHTML = `
            <td><b>TOTAL</b></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td><b>${this.data.beneficio}</b></td>
        `
        tbody.appendChild(totalRow)
    }

    renderDividendos() {
        const tbody = this.container.querySelector('.dividendos-tbody')
        if (!tbody) return

        tbody.innerHTML = ''

        this.data.dividendos.forEach(cv => {
            const tr = document.createElement('tr')
            tr.innerHTML = `
                <td>${cv.concepto}</td>
                <td>${cv.fecha_valor}</td>
                <td>${cv.importe}</td>
            `
            tbody.appendChild(tr)
        })

        const totalRow = document.createElement('tr')
        totalRow.innerHTML = `
            <td><b>TOTAL</b></td>
            <td></td>
            <td><b>${this.data.beneficio_dividendos}</b></td>
        `
        tbody.appendChild(totalRow)
    }
}

export class DiferentesAcciones {
    constructor() {
        this.data = []
        this.container = document.getElementById('acciones-list')
    }

    async init() {
        try {
            const res = await fetch(`/diferentes_acciones`)
            if (!res.ok) {
                throw new Error(`HTTP ${res.status}`)
            }
            this.data = await res.json()
            this.render()
        } catch (e) {
            console.error('Error fetching acciones:', e)
        }
    }

    render() {
        if (!this.container) return

        this.container.innerHTML = ''

        this.data.forEach(d => {
            const li = document.createElement('li')
            const a = document.createElement('a')
            a.href = `/static/cartera_isin.html?isin=${d.isin}&selected_screen=cartera_accion`
            a.textContent = d.nombre
            li.appendChild(a)
            this.container.appendChild(li)
        })
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const app = new Application()

    const yearReport = new YearReport()
    app.registerScreen('year_report', yearReport)

    const carteraScreen = new CarteraScreen()
    app.registerScreen('cartera_accion', carteraScreen)

    const diferentesAcciones = new DiferentesAcciones()
    diferentesAcciones.init()

    app.init()
})
