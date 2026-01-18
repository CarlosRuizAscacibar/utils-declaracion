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

#### Manual Import Scripts
```bash
# Import stock operations
python loader/persistir_ops.py

# Import bank movements
python loader/persistir_movs.py

# Import from specific brokers
python loader/broker_myinvestor.py
python loader/evo.py
```

#### Automated Data Retrieval
The web interface provides automated data retrieval from supported brokers:

- **Load Files**: Process all configured data files automatically
- **Get MyInvestor Data**: Retrieve orders and bank movements from MyInvestor platform using your credentials

To use MyInvestor data retrieval:
1. Navigate to "Get MyInvestor Data" in the web interface
2. Enter your MyInvestor username and password
3. Click "Get MyInvestor Data" to retrieve and import your data automatically

## Recent Changes

### v1.1.0 - MyInvestor Data Integration
- **New Feature**: Added MyInvestor data retrieval screen
  - Secure credential input for MyInvestor platform
  - Automated retrieval of orders and bank movements
  - Integrated with existing data processing pipeline
- **API Enhancement**: New `/get_investor_data` endpoint
  - Accepts username/password credentials
  - Runs both orders and movements retrieval scripts
  - Returns combined status and output
- **Frontend Updates**:
  - New investor data screen with form validation
  - Enhanced UI with loading states and error handling
  - Comprehensive test coverage (unit and e2e tests)
- **Backend Improvements**:
  - Modified MyInvestor scripts to accept command-line credentials
  - Enhanced error handling and status reporting

## Documentation

- [API Reference](docs/API.md)
- [Database Backup System](docs/BACKUP.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Configuration](docs/CONFIGURATION.md)
- [Frontend Documentation](docs/FRONTEND.md)
- [Changelog](CHANGELOG.md)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

See LICENSE file for details.