# Stock Portfolio Manager

A web application for managing and tracking stock portfolio data with support for multiple brokers and automated database backups.

## Features

- **Portfolio Overview**: View all stocks in your portfolio with current values
- **Detailed Stock Analysis**: Comprehensive view of individual stock performance, including:
  - Transaction history (buys/sells)
  - Dividend payments
  - Profit/loss calculations
  - Real-time valuations
- **Multi-Broker Support**: Import data from various brokers (MyInvestor, EVO, Interactive Brokers, etc.)
- **Yearly Reporting**: Annual performance reports with gains/losses analysis
- **Database Backup System**: Automated SQLite database backups with configurable locations
- **Modern Web Interface**: Single-page application with responsive design
- **Comprehensive Test Suite**: Both backend and frontend tests included

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend tests only)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd utils-declaracion
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend test dependencies** (optional)
   ```bash
   cd tests/frontend
   npm install
   cd ../..
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env  # If example exists, otherwise create .env
   ```

   Edit `.env` with your settings:
   ```bash
   # Database
   PERSONAL_DATABASE=./data/portfolio.db

   # Backup settings
   BACKUP_FOLDER=./backups

   # Broker data source paths
   SOURCE_EVO_FILES=./data/evo/
   SOURCE_MY_INVESTOR_FILES=./data/myinvestor/
   SPLIT_PATH=./data/splits/
   ```

### Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   ```
   http://localhost:5000
   ```

### Data Import

The application supports importing data from various sources:

```bash
# Import stock operations
python loader/persistir_ops.py

# Import bank movements
python loader/persistir_movs.py

# Import from specific brokers
python loader/broker_myinvestor.py
python loader/evo.py
```

## API Reference

### Portfolio Data

#### Get All Stocks
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

#### Get Stock Details
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

#### Get Yearly Report
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

### Database Management

#### Create Database Backup
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

## Database Backup System

The application includes a robust backup system for the SQLite database.

### Features

- **Automated Backups**: Create backups via API endpoint
- **Dated Filenames**: `backup_YYYYMMDD.db` format
- **Overwrite Protection**: Same-day backups replace existing files
- **Configurable Location**: Set backup directory via `BACKUP_FOLDER` environment variable
- **Safe Operation**: Uses SQLite-compatible file copying

### Usage

#### Manual Backup
```bash
curl -X POST http://localhost:5000/backup
```

#### Automated Backup
Set up a cron job for daily backups:
```bash
# Add to crontab (crontab -e)
0 2 * * * curl -X POST http://localhost:5000/backup
```

#### Environment Configuration
```bash
# In .env file
BACKUP_FOLDER=./backups
```

### Backup Contents

The backup includes all portfolio data:
- Stock transactions (purchases/sales)
- Dividend payments and records
- Broker information
- Currency exchange rates
- Stock split operations
- Market data and valuations

### Recovery

To restore from a backup:
```bash
# Stop the application
# Replace the database file
cp ./backups/backup_20240111.db "$PERSONAL_DATABASE"
# Restart the application
```

## Development

### Project Structure

```
├── app.py                    # Main Flask application
├── servicios/               # Business logic services
│   ├── backup_service.py    # Database backup functionality
│   ├── operations_from_db.py # Database operations
│   └── ...
├── modelos/                 # Data models and constants
├── loader/                  # Data import utilities
├── static/                  # Frontend assets
│   ├── main.js             # SPA application logic
│   ├── index.html          # Main HTML page
│   └── style.css           # Stylesheets
├── tests/                   # Test suite
│   ├── servicios/          # Backend tests
│   └── frontend/           # Frontend tests
└── requirements.txt         # Python dependencies
```

### Running Tests

#### Backend Tests
```bash
# Run all Python tests
python -m unittest discover tests/

# Run specific test
python -m unittest tests.servicios.test_backup_service
```

#### Frontend Tests

See [FRONTEND.md](docs/FRONTEND.md) for detailed frontend development and testing instructions.

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused on single responsibilities

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PERSONAL_DATABASE` | SQLite database file path | Required |
| `BACKUP_FOLDER` | Database backup directory | `./backups` |
| `SOURCE_EVO_FILES` | EVO broker data directory | - |
| `SOURCE_MY_INVESTOR_FILES` | MyInvestor data directory | - |
| `SPLIT_PATH` | Stock split data file | - |

### Database Schema

The SQLite database contains tables for:
- **operations**: Stock transactions
- **bank_movements**: Bank account movements
- **dividends**: Dividend payments
- **splits**: Stock split operations
- **currency_rates**: Exchange rates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

See LICENSE file for details.