# Database Backup System

The application includes a robust backup system for the SQLite database.

## Features

- **Automated Backups**: Create backups via API endpoint
- **Dated Filenames**: `backup_YYYYMMDD.db` format
- **Overwrite Protection**: Same-day backups replace existing files
- **Configurable Location**: Set backup directory via `BACKUP_FOLDER` environment variable
- **Safe Operation**: Uses SQLite-compatible file copying
- **Last Backup Tracking**: API endpoint to check when last backup was performed

## Usage

### Manual Backup
```bash
curl -X POST http://localhost:5000/backup
```

### Automated Backup
Set up a cron job for daily backups:
```bash
# Add to crontab (crontab -e)
0 2 * * * curl -X POST http://localhost:5000/backup
```

### Check Last Backup
```bash
curl http://localhost:5000/backup/last
```

### Environment Configuration
```bash
# In .env file
BACKUP_FOLDER=./backups
```

## Backup Contents

The backup includes all portfolio data:
- Stock transactions (purchases/sales)
- Dividend payments and records
- Broker information
- Currency exchange rates
- Stock split operations
- Market data and valuations

## Recovery

To restore from a backup:
```bash
# Stop the application
# Replace the database file
cp ./backups/backup_20240111.db "$PERSONAL_DATABASE"
# Restart the application
```

## Implementation Details

- Backups are stored in the directory specified by `BACKUP_FOLDER`
- Each backup creates a file named `backup_YYYYMMDD.db`
- The last backup timestamp is stored in `last_backup.txt` in the backup folder
- The system uses `shutil.copy2` to preserve file metadata