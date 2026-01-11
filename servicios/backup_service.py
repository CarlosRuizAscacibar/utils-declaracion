import os
import shutil
from datetime import datetime
from modelos.constants import EnvironmentVariableNames

def create_database_backup():
    """
    Creates a backup of the SQLite database with today's date in the filename.
    Overwrites any existing backup from the same day.

    Returns:
        tuple: (success: bool, message: str, path: str or None)
    """
    try:
        db_path = os.getenv(EnvironmentVariableNames.PERSONAL_DATABASE)
        if not db_path or not os.path.exists(db_path):
            return False, "Database not found", None

        backup_folder = os.getenv(EnvironmentVariableNames.BACKUP_FOLDER, './backups')
        os.makedirs(backup_folder, exist_ok=True)

        today = datetime.now().strftime("%Y%m%d")
        backup_filename = f"backup_{today}.db"
        backup_path = os.path.join(backup_folder, backup_filename)

        # Copy the database file
        shutil.copy2(db_path, backup_path)

        return True, f"Backup created: {backup_filename}", backup_path
    except Exception as e:
        return False, str(e), None