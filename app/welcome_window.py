import re
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QMessageBox
from utils.database_manager import DatabaseManager

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
            db_manager.create_user_table()
            db_manager.create_prediction_table()
        except Exception as e:
            # Display an error message if something goes wrong
            QMessageBox.critical(self, "Database Error", f"Failed to create database: {str(e)}", QMessageBox.Ok)

def is_valid_email(email):
    # Updated email validation using regular expression
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+$'
    return re.match(pattern, email) is not None