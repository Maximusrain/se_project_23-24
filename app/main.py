import csv
import re
import sys
from datetime import datetime

from PyQt5.QtGui import QFont
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit, QStackedWidget, QMessageBox, \
    QMainWindow, QVBoxLayout, QCheckBox
from ..utils.DatabaseManager import DatabaseManager
from ..ml_model.model import predd, loaded_rf


class WelcomePage(QDialog):
    def __init__(self, widget):
        super(WelcomePage, self).__init__()
        loadUi("ui/welcome.ui", self)
        self.widget = widget
        self.login.clicked.connect(self.go_to_login)
        self.signup.clicked.connect(self.go_to_signup)
        self.create_database()

    def go_to_login(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def go_to_signup(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 2)

    def create_database(self):
        db_manager = DatabaseManager()
        try:
            # Attempt to create the database and the user table
            db_manager.create_database()
            db_manager.create_table()
        except Exception as e:
            # Display an error message if something goes wrong
            QMessageBox.critical(self, "Database Error", f"Failed to create database: {str(e)}", QMessageBox.Ok)


def is_valid_email(email):
    # Email validation using regular expression
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


class LoginPage(QDialog):
    def __init__(self, widget):
        super(LoginPage, self).__init__()
        loadUi("ui/login.ui", self)
        self.widget = widget
        self.PasswordLine.setEchoMode(QLineEdit.Password)
        self.login_btn.clicked.connect(self.loginfunction)
        self.goback_btn.clicked.connect(self.go_back)

    # Inside the loginfunction of LoginPage
    def loginfunction(self):
        try:
            user = self.EmailLine.text()
            password = self.PasswordLine.text()

            if len(user) == 0 or len(password) == 0:
                self.label_invalid_line.setText("Please input fields.")
            elif not is_valid_email(user):
                self.label_invalid_line.setText("Invalid email address.")
            else:
                db_manager = DatabaseManager()
                if db_manager.check_user_credentials(user, password):
                    self.label_invalid_line.setText("Login successful.")
                    print(f"Login successful. User: {user}")

                    # Access the main window's central widget and switch content
                    main_window = MainWindow(self.widget)  # Instantiate your MainWindow class
                    self.widget.addWidget(main_window)

                    # Ensure the index is correct for MainWindow
                    main_window_index = self.widget.indexOf(main_window)
                    self.widget.setCurrentIndex(main_window_index)

                    # Close or hide the login page
                    self.accept()  # This will close the dialog
                else:
                    self.label_invalid_line.setText("Invalid email or password.")
                    print("Invalid email or password.")
        except Exception as e:
            print(f"Error during login: {str(e)}")

    def go_back(self):
        # Clear all the input fields
        self.EmailLine.clear()
        self.PasswordLine.clear()
        self.label_invalid_line.clear()
        # Set the current index to go back
        self.widget.setCurrentIndex(self.widget.currentIndex() - 1)


class SignupPage(QDialog):
    def __init__(self, widget):
        super(SignupPage, self).__init__()
        loadUi("ui/signup.ui", self)
        self.widget = widget
        self.Password_line.setEchoMode(QLineEdit.Password)
        self.Password_confirm.setEchoMode(QLineEdit.Password)
        self.create_btn.clicked.connect(self.signupfunction)
        self.goback_btn.clicked.connect(self.go_back)

    def signupfunction(self):
        user = self.Email_line.text()
        password = self.Password_line.text()
        password_con = self.Password_confirm.text()
        if len(user) == 0 or len(password) == 0 or len(password_con) == 0:
            self.label_invalid_line.setText("Please input all fields.")
        elif not is_valid_email(user):
            self.label_invalid_line.setText("Invalid email.")
        elif password != password_con:
            self.label_invalid_line.setText("Passwords do not match.")
        else:
            try:
                db_manager = DatabaseManager()
                db_manager.register_user(user, password)
                self.label_invalid_line.setText("Signup successful.")
                print(f"Signup successful. User: {user}, Hashed Password: {password}")
            except Exception as e:
                self.label_invalid_line.setText(f"Error: {str(e)}")
                print(f"Error during signup: {str(e)}")

    def go_back(self):
        # Clear all the input fields
        self.Email_line.clear()
        self.Password_line.clear()
        self.Password_confirm.clear()
        self.label_invalid_line.clear()
        # Set the current index to go back
        self.widget.setCurrentIndex(self.widget.currentIndex() - 2)


class MainWindow(QMainWindow):
    def __init__(self, widget):
        super(MainWindow, self).__init__()
        self.scrollArea = None
        self.predict_button = None
        self.result_text_edit = None
        loadUi("ui/main_window.ui", self)
        self.widget = widget
        self.load_symptoms()
        self.predict_button.clicked.connect(self.on_predict_button_clicked)

    def on_predict_button_clicked(self):
        # Get the symptoms from the checkboxes
        selected_symptoms = self.get_selected_symptoms()

        # Get prediction
        prediction_result = predd(
            loaded_rf,
            *selected_symptoms
        )

        # Display the prediction result in the text window
        self.result_text_edit.setPlainText(prediction_result)

        # Save the prediction result in the database
        self.save_to_database(prediction_result)

    def save_to_database(self, prediction_result):
        db_manager = DatabaseManager()

        # Get the current user (replace 'get_current_user' with the actual method)
        current_user = db_manager.get_current_user()

        # Save the prediction in the database with user and timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db_manager.save_prediction(current_user, prediction_result, timestamp)

    def clean_symptom_name(self, name):
        # Remove underscores and capitalize the first letter
        return name.replace("_", " ").capitalize()

    def load_symptoms(self):
        symptom_file = "data/Symptom-severity.csv"

        # Create a widget to hold checkboxes
        widget = QWidget(self.scrollArea)
        layout = QVBoxLayout(widget)

        try:
            with open(symptom_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                symptoms = [self.clean_symptom_name(row['Symptom']) for row in reader]

                # Sort symptoms alphabetically
                symptoms.sort()

                for symptom in symptoms:
                    checkbox = QCheckBox(symptom)

                    # Set font and remove background
                    checkbox.setStyleSheet("QCheckBox { background-color: none; }")
                    checkbox.setFont(QFont("Century Gothic", 11))

                    layout.addWidget(checkbox)

        except FileNotFoundError:
            print(f"File {symptom_file} not found.")

        self.scrollArea.setWidget(widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    welcome = WelcomePage(widget)
    login = LoginPage(widget)
    signup = SignupPage(widget)

    widget.addWidget(welcome)
    widget.addWidget(login)
    widget.addWidget(signup)

    widget.setFixedWidth(1000)
    widget.setFixedHeight(800)
    widget.show()

    sys.exit(app.exec_())
