import unittest
from unittest.mock import MagicMock, patch, call
import pymysql
from utils.database_manager import DatabaseManager  # Import your DatabaseManager class from your module

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Create a mock DatabaseManager instance with dummy connection parameters
        self.db_manager = DatabaseManager(host='localhost', user='test_user', password='test_password', database='test_db')

    @patch('pymysql.connect')
    def test_create_database(self, connect_mock):
        # Call the create_database method
        self.db_manager.create_database()

        # Check if pymysql.connect method was called with correct parameters
        connect_mock.assert_called_once_with(host='localhost', user='test_user', password='test_password')

if __name__ == '__main__':
    unittest.main()