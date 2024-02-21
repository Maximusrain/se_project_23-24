import csv
import sqlite3

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
        with pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database) as conn:
            cursor = conn.cursor()
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')

    def create_user_table(self):
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

    def create_prediction_table(self):
        # Method to create a table for predictions (PredictionID, UserID, Disease, Timestamp, Symptoms)
        with pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prediction (
                    PredictionID INT AUTO_INCREMENT NOT NULL,
                    UserID INT NOT NULL,
                    Disease VARCHAR(255) NOT NULL,
                    Symptoms TEXT,
                    Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    PRIMARY KEY (PredictionID),
                    FOREIGN KEY (UserID) REFERENCES user(UserID) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
            ''')
            conn.commit()

    def add_prediction(self, user_name, disease_name, symptoms):
        try:
            with pymysql.connect(host=self.host, user=self.user, password=self.password,
                                 database=self.database) as conn:
                cursor = conn.cursor()
                # Convert the list of symptoms into a string
                symptoms_str = ','.join(symptoms)
                # Insert a new prediction into the prediction table
                cursor.execute('''
                    INSERT INTO prediction (UserID, Disease, Symptoms, Timestamp)
                    SELECT UserID, %s, %s, CURRENT_TIMESTAMP
                    FROM user
                    WHERE Email = %s
                ''', (disease_name, symptoms_str, user_name))
                conn.commit()
                print("Prediction added successfully.")
        except pymysql.Error as e:
            print(f"Error adding prediction: {str(e)}")

    def get_user_predictions(self, user_name):
        try:
            with pymysql.connect(host=self.host, user=self.user, password=self.password,
                                 database=self.database) as conn:
                cursor = conn.cursor()
                # Retrieve predictions for the user
                cursor.execute('''
                    SELECT p.PredictionID, p.Disease, p.Symptoms, p.Timestamp
                    FROM prediction p
                    INNER JOIN user u ON p.UserID = u.UserID
                    WHERE u.Email = %s
                ''', (user_name,))
                predictions = cursor.fetchall()
                return predictions
        except pymysql.Error as e:
            print(f"Error fetching predictions: {str(e)}")
            return []

    def delete_prediction_by_id(self, prediction_id):
        try:
            with pymysql.connect(host=self.host, user=self.user, password=self.password,
                                 database=self.database) as conn:
                cursor = conn.cursor()
                # Delete the prediction from the prediction table based on its ID
                cursor.execute('DELETE FROM prediction WHERE PredictionID = %s', (prediction_id,))
                conn.commit()
                print("Prediction deleted successfully.")
        except pymysql.Error as e:
            print(f"Error deleting prediction: {str(e)}")

    def register_user(self, email, password):
        try:
            # Check if the user already exists
            if self.user_exists(email):
                raise ValueError("User already exists.")

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

    def user_exists(self, email):
        # Check if the user already exists in the database
        with pymysql.connect(host=self.host, user=self.user, password=self.password,
                             database=self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM user WHERE Email = %s', (email,))
            result = cursor.fetchone()
            return result[0] > 0

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

    def get_recommendations(self, disease):
        try:
            # Read recommendations from the CSV file
            with open('D:\POLSL\SE\DiseaseSymptomPrediction\data\symptom_precaution.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['Disease'] == disease:
                        # Extract recommendations for the specified disease
                        recommendations = []
                        for i in range(1, 5):
                            precaution_key = f'Precaution_{i}'
                            precaution = row.get(precaution_key)
                            if precaution:
                                precaution = precaution.capitalize()
                                recommendations.append(precaution)
                        return recommendations
        except Exception as e:
            print(f"Error reading recommendations: {str(e)}")
            return []
