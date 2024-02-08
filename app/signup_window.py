from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QLineEdit
from utils.DatabaseManager import DatabaseManager
from welcome_window import is_valid_email

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