import os
import tempfile
import unittest
import shutil
from datetime import datetime

from servicios.backup_service import create_database_backup
from modelos.constants import EnvironmentVariableNames


class TestBackupService(unittest.TestCase):
    def setUp(self):
        # Use a fixed backup folder within tests directory
        self.backup_folder = os.path.join(os.path.dirname(__file__), '..', 'tmp', 'backup')
        os.makedirs(self.backup_folder, exist_ok=True)

        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.db')
        with os.fdopen(self.db_fd, 'w') as f:
            f.write('test database content')

        # Set environment variables
        os.environ[EnvironmentVariableNames.PERSONAL_DATABASE] = self.db_path
        os.environ[EnvironmentVariableNames.BACKUP_FOLDER] = self.backup_folder

    def tearDown(self):
        # Clean up temporary database file
        try:
            os.unlink(self.db_path)
        except FileNotFoundError:
            pass  # File was already removed in a test
        # Clean up backup files but keep the directory structure
        for filename in os.listdir(self.backup_folder):
            file_path = os.path.join(self.backup_folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception:
                pass  # Ignore errors during cleanup

    def test_successful_backup(self):
        """Test that backup creates a file with today's date"""
        success, message, path = create_database_backup()

        self.assertTrue(success)
        self.assertIsNotNone(path)
        assert path is not None  # Type assertion for mypy
        self.assertTrue(os.path.exists(path))

        # Check filename format
        today = datetime.now().strftime("%Y%m%d")
        expected_filename = f"backup_{today}.db"
        self.assertTrue(path.endswith(expected_filename))

        # Check content is copied correctly
        with open(path, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'test database content')

        # Check message
        self.assertIn(f"backup_{today}.db", message)

    def test_backup_folder_creation(self):
        """Test that backup works with existing folder"""
        # The backup folder should already exist from setUp
        self.assertTrue(os.path.exists(self.backup_folder))

        success, message, path = create_database_backup()

        self.assertTrue(success)
        self.assertIsNotNone(path)
        self.assertTrue(os.path.exists(path))

    def test_overwrite_existing_backup(self):
        """Test that backups from the same day overwrite previous ones"""
        # Create first backup
        success1, message1, path1 = create_database_backup()
        self.assertTrue(success1)

        # Modify the database content
        with open(self.db_path, 'w') as f:
            f.write('modified database content')

        # Create second backup (should overwrite)
        success2, message2, path2 = create_database_backup()
        self.assertTrue(success2)

        # Should be the same path
        self.assertEqual(path1, path2)

        # Check content is the new content
        with open(path2, 'r') as f:
            content = f.read()
        self.assertEqual(content, 'modified database content')

    def test_database_not_found(self):
        """Test error when database file doesn't exist"""
        # Remove the database file
        os.unlink(self.db_path)

        success, message, path = create_database_backup()

        self.assertFalse(success)
        self.assertEqual(message, "Database not found")
        self.assertIsNone(path)

    def test_database_path_not_set(self):
        """Test error when PERSONAL_DATABASE environment variable is not set"""
        del os.environ[EnvironmentVariableNames.PERSONAL_DATABASE]

        success, message, path = create_database_backup()

        self.assertFalse(success)
        self.assertEqual(message, "Database not found")
        self.assertIsNone(path)

    def test_backup_folder_default(self):
        """Test that backup uses default folder when BACKUP_FOLDER is not set"""
        del os.environ[EnvironmentVariableNames.BACKUP_FOLDER]

        success, message, path = create_database_backup()

        self.assertTrue(success)
        self.assertIsNotNone(path)
        # Should use './backups' as default
        self.assertIn('./backups', path)
        self.assertTrue(os.path.exists(path))

        # Clean up the file created in the default location
        os.unlink(path)


if __name__ == '__main__':
    unittest.main()