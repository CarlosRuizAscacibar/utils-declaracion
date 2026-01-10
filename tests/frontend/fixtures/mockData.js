export const carteraResponse = {
  isin: 'US5949724083',
  acciones_actual: 100,
  valor_actual: 15000.50,
  operaciones: [
    {
      id: 1,
      fecha: '2024-01-15',
      tipo: 1,
      cantidad: 50,
      divisa: 'EUR',
      precio_unitario: 150.00,
      importe_neto: 7500.00,
      broker: 'Degiro',
      dias_ultima_venta: 30,
      restantes: 50,
      nombre: 'Apple Inc.'
    },
    {
      id: 2,
      fecha: '2024-02-01',
      tipo: 2,
      cantidad: 25,
      divisa: 'EUR',
      precio_unitario: 180.00,
      importe_neto: 4500.00,
      broker: 'Degiro',
      dias_ultima_venta: 15,
      restantes: 25,
      nombre: 'Apple Inc.'
    },
    {
      id: 3,
      fecha: '2024-03-10',
      tipo: 3,
      cantidad: 0,
      divisa: 'USD',
      precio_unitario: 0.50,
      importe_neto: 25.00,
      broker: 'Degiro',
      dias_ultima_venta: 0,
      restantes: 25,
      nombre: 'Apple Inc.'
    },
    {
      id: 4,
      fecha: '2024-04-01',
      tipo: 4,
      numOriginal: 25,
      numDestino: 50,
      cantidad: 0,
      divisa: 'EUR',
      precio_unitario: 0,
      importe_neto: 0,
      broker: 'Degiro',
      dias_ultima_venta: 0,
      restantes: 50,
      nombre: 'Apple Inc.'
    }
  ],
  compra_ventas_report: [
    {
      fecha_compra: '2024-01-15',
      precio_unitario_compra: 150.00,
      fecha_venta: '2024-02-01',
      precio_unitario_venta: 180.00,
      ganancia_perdida_eur: 750.00
    }
  ],
  dividendos: [
    {
      concepto: 'Dividendo Q1 2024',
      fecha_valor: '2024-03-10',
      importe: 25.00
    }
  ],
  beneficio_dividendos: 25.00
}

export const yearReportResponse = {
  year: 2024,
  beneficio: 5000.00,
  beneficio_dividendos: 1000.00,
  compra_ventas_report: [
    {
      nombre: 'Apple Inc.',
      fecha_compra: '2024-01-15',
      precio_unitario_compra: 150.00,
      fecha_venta: '2024-02-01',
      precio_unitario_venta: 180.00,
      ganancia_perdida_eur: 750.00
    },
    {
      nombre: 'Microsoft Corp.',
      fecha_compra: '2024-03-01',
      precio_unitario_compra: 300.00,
      fecha_venta: '2024-04-15',
      precio_unitario_venta: 350.00,
      ganancia_perdida_eur: 1250.00
    }
  ],
  dividendos: [
    {
      concepto: 'Dividendo Apple Q1',
      fecha_valor: '2024-03-10',
      importe: 25.00
    },
    {
      concepto: 'Dividendo Apple Q2',
      fecha_valor: '2024-06-15',
      importe: 30.00
    },
    {
      concepto: 'Dividendo Microsoft Q1',
      fecha_valor: '2024-03-20',
      importe: 50.00
    }
  ]
}

export const diferentesAccionesResponse = [
  {
    isin: 'US5949724083',
    nombre: 'Apple Inc.'
  },
  {
    isin: 'US5949181045',
    nombre: 'Microsoft Corp.'
  },
  {
    isin: 'US02079K3059',
    nombre: 'Alphabet Inc.'
  }
]

export const carteraEmptyResponse = {
  isin: 'US5949724083',
  acciones_actual: 0,
  valor_actual: 0,
  operaciones: [],
  compra_ventas_report: [],
  dividendos: [],
  beneficio_dividendos: 0
}

export const yearReportEmptyResponse = {
  year: 2025,
  beneficio: 0,
  beneficio_dividendos: 0,
  compra_ventas_report: [],
  dividendos: []
}
