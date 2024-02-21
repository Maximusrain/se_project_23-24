import unittest
import pymysql

from utils.database_manager import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # Connect to the test database
        self.connection = pymysql.connect(host='localhost', user='root', password='',
                                          database='disease_prediction', port=3306)
        self.cursor = self.connection.cursor()
        # Create necessary tables if they don't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS user (
                UserID INT AUTO_INCREMENT PRIMARY KEY,
                UserPassword VARCHAR(100) NOT NULL,
                Email VARCHAR(255) NOT NULL UNIQUE
            )
        ''')
        self.connection.commit()

        # Initialize the DatabaseManager instance
        self.db_manager = DatabaseManager()

    def test_create_database(self):
        # Call the create_database method
        self.db_manager.create_database()

        # Check if the database exists after calling create_database
        db_exists_after = self.check_database_exists()

        # Assert that the database exists after calling create_database
        self.assertTrue(db_exists_after)

    def check_database_exists(self):
        try:
            # Connect to MySQL server without specifying a database
            with pymysql.connect(host=self.db_manager.host, user=self.db_manager.user,
                                 password=self.db_manager.password) as conn:
                cursor = conn.cursor()
                # Execute a query to check if the database exists
                cursor.execute(f"SHOW DATABASES LIKE '{self.db_manager.database}'")
                return cursor.fetchone() is not None
        except pymysql.Error as e:
            print(f"Error checking database existence: {str(e)}")
            return False

    def tearDown(self):
        try:
            # Delete the test user from the user table
            test_user_email = "test@example.com"
            self.cursor.execute("DELETE FROM user WHERE Email = %s", (test_user_email,))
            self.connection.commit()
            print("Test user deleted successfully.")
        except Exception as e:
            print(f"Error deleting test user: {e}")
        finally:
            # Close the database connection
            self.connection.close()

    def test_register_user(self):
        # Test user registration
        email = "test@example.com"
        password = "password"

        # Register a new user
        self.db_manager.register_user(email, password)

        # Check if the user was successfully registered by querying the database
        self.assertTrue(self.db_manager.user_exists(email))

    def test_delete_prediction_by_id(self):
        # Create a user
        user_name = "testuser@example.com"

        # Add a prediction for the user
        disease_name = "Flu"
        symptoms = ["Fever", "Cough"]
        self.db_manager.add_prediction(user_name, disease_name, symptoms)

        # Get the ID of the prediction
        self.cursor.execute(
            'SELECT PredictionID FROM prediction WHERE UserID = (SELECT UserID FROM user WHERE Email = %s)',
            (user_name,))
        prediction_row = self.cursor.fetchone()
        prediction_id = prediction_row[0] if prediction_row else None
        print("Prediction ID before deletion:", prediction_id)

        # Delete the prediction
        self.db_manager.delete_prediction_by_id(prediction_id)
        print("Prediction deleted successfully.")

        # Create a new cursor and connection to the database
        new_connection = pymysql.connect(host='localhost', user='root', password='', database='disease_prediction',
                                         port=3306)
        new_cursor = new_connection.cursor()

        # Check if the prediction was deleted by querying the database
        new_cursor.execute('SELECT * FROM prediction WHERE PredictionID = %s', (prediction_id,))
        deletion_result = new_cursor.fetchone()
        print("Prediction deletion result:", deletion_result)

        # Check the prediction count for the user after deletion
        new_cursor.execute(
            'SELECT COUNT(*) FROM prediction WHERE UserID = (SELECT UserID FROM user WHERE Email = %s)',
            (user_name,))
        prediction_count_after_deletion = new_cursor.fetchone()[0]
        print("Prediction count after deletion:", prediction_count_after_deletion)

        # Close the new cursor and connection
        new_cursor.close()
        new_connection.close()

        # Assert that the prediction was successfully deleted
        self.assertIsNone(deletion_result, "Prediction should have been deleted")
        self.assertEqual(prediction_count_after_deletion, 0, "All predictions for the user should have been deleted")

    def test_get_recommendations_if_disease_exists(self):
        # Test getting recommendations for a known disease
        disease = "Diabetes "
        recommendations = self.db_manager.get_recommendations(disease)
        expected_recommendations = ["Have balanced diet", "Exercise", "Consult doctor", "Follow up"]
        self.assertEqual(recommendations, expected_recommendations)

    def test_get_recommendations_if_disease_does_not_exist(self):
        # Test getting recommendations for an unknown disease
        unknown_disease = "Unknown"
        recommendations = self.db_manager.get_recommendations(unknown_disease)
        self.assertEqual(recommendations, None)

if __name__ == "__main__":
    unittest.main()
