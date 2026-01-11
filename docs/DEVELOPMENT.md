# Development Guide

## Project Structure

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

## Running Tests

### Backend Tests
```bash
# Run all Python tests
python -m unittest discover tests/

# Run specific test
python -m unittest tests.servicios.test_backup_service
```

### Frontend Tests
See [FRONTEND.md](FRONTEND.md) for detailed frontend development and testing instructions.

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused on single responsibilities