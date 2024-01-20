import bcrypt
import pymysql

class DatabaseManager:
    def __init__(self, host='localhost', user='root',
                 password='', database='disease_prediction'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def create_database(self):
        # Connect to the MySQL server without specifying a database
        with pymysql.connect(host=self.host, user=self.user, password=self.password) as conn:
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')

    def create_table(self):
        # Create a table for user data (UserID, UserPassword, Email)
        with pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user (
                    UserID INT AUTO_INCREMENT NOT NULL,
                    UserPassword VARCHAR(100) NOT NULL,
                    Email VARCHAR(255) NOT NULL,
                    PRIMARY KEY (UserID),
                    UNIQUE KEY Email (Email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            ''')
            conn.commit()

    def register_user(self, email, password):
        try:
            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert the user data into the database
            with pymysql.connect(host=self.host, user=self.user, password=self.password,
                                 database=self.database) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO user (UserPassword, Email) VALUES (%s, %s)', (hashed_password, email))
                conn.commit()

            print(f"User registered successfully. User: {email}")
        except pymysql.Error as e:
            print(f"Database error during registration: {str(e)}")
            raise pymysql.Error(f"Database error during registration: {str(e)}")
        except Exception as e:
            print(f"Error during registration: {str(e)}")
            raise Exception(f"Error during registration: {str(e)}")

    def check_user_credentials(self, email, password):
        # Retrieve hashed password from the database based on email
        with pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT UserPassword FROM user WHERE Email = %s', (email,))
            result = cursor.fetchone()

            if result:
                # Check if the entered password matches the stored hash
                stored_hash = result[0].encode('utf-8')
                return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

        return False