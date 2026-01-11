# Configuration

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PERSONAL_DATABASE` | SQLite database file path | Required |
| `BACKUP_FOLDER` | Database backup directory | `./backups` |
| `SOURCE_EVO_FILES` | EVO broker data directory | - |
| `SOURCE_MY_INVESTOR_FILES` | MyInvestor data directory | - |
| `SPLIT_PATH` | Stock split data file | - |

## Database Schema

The SQLite database contains tables for:
- **operations**: Stock transactions
- **bank_movements**: Bank account movements
- **dividends**: Dividend payments
- **splits**: Stock split operations
- **currency_rates**: Exchange rates