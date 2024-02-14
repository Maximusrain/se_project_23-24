from PyQt5.QtWidgets import QDialog, QLineEdit
from PyQt5.uic import loadUi

from main_window import MainWindow
from utils.database_manager import DatabaseManager
from welcome_window import is_valid_email


class LoginPage(QDialog):
    logged_in_user_email = None
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
                    self.logged_in_user_email = user

                    # Access the main window's central widget and switch content
                    main_window = MainWindow(self.widget, self.logged_in_user_email)  # Instantiate your MainWindow class
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