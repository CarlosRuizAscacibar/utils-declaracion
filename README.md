# Stock Portfolio Manager

A web application for managing and tracking stock portfolio data with support for multiple brokers and automated database backups.

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

## Documentation

- [API Reference](docs/API.md)
- [Database Backup System](docs/BACKUP.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Configuration](docs/CONFIGURATION.md)
- [Frontend Documentation](docs/FRONTEND.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

See LICENSE file for details.