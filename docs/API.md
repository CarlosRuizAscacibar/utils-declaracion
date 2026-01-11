# API Reference

## Portfolio Data

### Get All Stocks
```http
GET /diferentes_acciones
```

**Response:**
```json
[
  {
    "isin": "US0378331005",
    "nombre": "Apple Inc."
  },
  {
    "isin": "US5949181045",
    "nombre": "Microsoft Corporation"
  }
]
```

### Get Stock Details
```http
GET /cartera/{isin}
```

**Response:**
```json
{
  "isin": "US0378331005",
  "operaciones": [
    {
      "fecha": "2024-01-15",
      "tipo": "COMPRA",
      "cantidad": 10,
      "precio_unitario": 150.00,
      "divisa": "EUR",
      "broker": "MYINVESTOR"
    }
  ],
  "acciones_actual": 10,
  "compra_ventas_report": [...],
  "dividendos": [...],
  "beneficio_dividendos": 25.00,
  "valor_actual": 1650.00
}
```

### Get Yearly Report
```http
GET /report/year/{year}
```

**Response:**
```json
{
  "year": "2024",
  "compra_ventas_report": [...],
  "dividendos": [...],
  "beneficio": 1250.50,
  "beneficio_dividendos": 150.25
}
```

### Get Last Backup Time
```http
GET /backup/last
```

**Response:**
```json
{
  "last_backup": "2024-01-15T14:30:00.123456"
}
```

## Database Management

### Create Database Backup
```http
POST /backup
```

**Response:**
```json
{
  "message": "Backup created: backup_20240111.db",
  "path": "./backups/backup_20240111.db"
}
```