import re
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit, QPushButton, QStackedWidget

class WelcomePage(QDialog):
    def __init__(self, widget):
        super(WelcomePage, self).__init__()
        loadUi("welcome.ui", self)
        self.widget = widget
        self.login.clicked.connect(self.go_to_login)
        self.signup.clicked.connect(self.go_to_signup)

    def go_to_login(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 1)

    def go_to_signup(self):
        self.widget.setCurrentIndex(self.widget.currentIndex() + 2)

def is_valid_email(email):
    # Email validation using regular expression
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

class LoginPage(QDialog):
    def __init__(self, widget):
        super(LoginPage, self).__init__()
        loadUi("login.ui", self)
        self.widget = widget
        self.PasswordLine.setEchoMode(QLineEdit.Password)
        self.login_btn.clicked.connect(self.loginfunction)
        self.goback_btn.clicked.connect(self.go_back)

    def loginfunction(self):
        user = self.EmailLine.text()
        password = self.PasswordLine.text()

        if len(user) == 0 or len(password) == 0:
            self.label_invalid_line.setText("Please input fields.")
        elif not is_valid_email(user):
            self.label_invalid_line.setText("Invalid email address.")
        else:
            self.label_invalid_line.setText("")
            print("connect with database")

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
        loadUi("signup.ui", self)
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
        elif not self.is_valid_email(user):
            self.label_invalid_line.setText("Invalid email address.")
        elif password != password_con:
            self.label_invalid_line.setText("Passwords do not match.")
        else:
            self.label_invalid_line.setText("")
            # Perform signup logic or connect to the database here
            print(f"Signup successful. User: {user}, Password: {password}")

    def go_back(self):
        # Clear all the input fields
        self.Email_line.clear()
        self.Password_line.clear()
        self.Password_confirm.clear()
        self.label_invalid_line.clear()
        # Set the current index to go back
        self.widget.setCurrentIndex(self.widget.currentIndex() - 2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QStackedWidget()

    welcome = WelcomePage(widget)
    login = LoginPage(widget)
    signup = SignupPage(widget)

    widget.addWidget(welcome)
    widget.addWidget(login)
    widget.addWidget(signup)

    widget.setFixedWidth(800)
    widget.setFixedHeight(600)
    widget.show()

    sys.exit(app.exec_())