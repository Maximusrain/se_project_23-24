import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from welcome_window import WelcomePage
from login_window import LoginPage
from signup_window import SignupPage

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