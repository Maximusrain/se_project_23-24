import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit, QPushButton


class WelcomePage(QDialog):#unfile welcome.ui to py
    def __init__(self):
        super(WelcomePage, self).__init__()
        loadUi("welcome.ui",self)
        self.login.clicked.connect(self.gotologin)#connect with login page opens new page
        self.signup.clicked.connect(self.gotosignup)




    def gotologin(self):
        login=LoginPage()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotosignup(self):
        signup=SignupPage()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex()+1)



class LoginPage(QDialog):#login page unfile to py
    def __init__(self):
        super(LoginPage,self).__init__()
        loadUi("login.ui",self)
        self.PasswordLine.setEchoMode(QLineEdit.Password)#hidden text for password
        self.login_btn.clicked.connect(self.loginfunction)



    def loginfunction(self):#here we connect with database
        user=self.EmailLine.text()
        password=self.PasswordLine.text()

        if len(user)==0 or len(password)==0:
            self.label_invalid_line.setText("Please input fields.")

        else :
             print("connect with database")
class SignupPage(QDialog):
    def __init__(self):
        super(SignupPage,self).__init__()
        loadUi("signup.ui",self)
        self.Password_line.setEchoMode(QLineEdit.Password)  # hidden text for password
        self.Password_confirm.setEchoMode(QLineEdit.Password)  # hidden text for password
        self.create_btn.clicked.connect(self.signupfunction)


    def signupfunction(self):#here we connect with database
        user=self.Email_line.text()
        password=self.Password_line.text()
        password_con=self.Password_confirm.text()

        if len(user)==0 or len(password)==0 or len(password_con)==0:
            self.label_invalid_line.setText("Please input fields.")

        else :
             print("connect with database")



#main
app=QApplication(sys.argv)
welcome=WelcomePage()
widget=QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedWidth(800)
widget.setFixedHeight(600)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("exit completed")

