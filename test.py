import bcrypt
from DatabaseManager import DatabaseManager

class TestDatabaseWriter:
    def __init__(self):
        # Create a DatabaseManager instance
        self.db_manager = DatabaseManager()

    def main(self):
        try:
            # Perform signup logic or connect to the database here
            user = "testuser@example.com"
            password = "testpassword"

            # Register the test user
            self.db_manager.register_user(user, password)
            print(f"Test user registered successfully. User: {user}, Hashed Password: {password}")
        except Exception as e:
            print(f"Error during registration: {str(e)}")

if __name__ == "__main__":
    test_writer = TestDatabaseWriter()
    test_writer.main()
