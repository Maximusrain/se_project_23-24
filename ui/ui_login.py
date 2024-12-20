# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(905, 737)
        Dialog.setStyleSheet("QDialog{\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 rgba(46, 117, 100, 255), stop:1 rgba(102, 221, 190, 255))}")
        self.EmailLine = QtWidgets.QLineEdit(Dialog)
        self.EmailLine.setGeometry(QtCore.QRect(310, 320, 281, 41))
        self.EmailLine.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"font: 12pt \"Century Gothic\";")
        self.EmailLine.setObjectName("EmailLine")
        self.label_invalid_line = QtWidgets.QLabel(Dialog)
        self.label_invalid_line.setGeometry(QtCore.QRect(330, 460, 231, 21))
        self.label_invalid_line.setStyleSheet("font: 14pt \"Century Gothic\"; color:red;")
        self.label_invalid_line.setText("")
        self.label_invalid_line.setAlignment(QtCore.Qt.AlignCenter)
        self.label_invalid_line.setObjectName("label_invalid_line")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(310, 380, 71, 31))
        self.label_4.setStyleSheet("font: 11pt \"Century Gothic\";")
        self.label_4.setObjectName("label_4")
        self.goback_btn = QtWidgets.QPushButton(Dialog)
        self.goback_btn.setGeometry(QtCore.QRect(330, 550, 231, 41))
        font = QtGui.QFont()
        font.setFamily("Century Gothic")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        self.goback_btn.setFont(font)
        self.goback_btn.setStyleSheet("border-radius:10px;\n"
"background-color: rgb(229, 232, 236);\n"
"\n"
"font: 14pt \"Century Gothic\";\n"
"")
        self.goback_btn.setObjectName("goback_btn")
        self.label_login = QtWidgets.QLabel(Dialog)
        self.label_login.setGeometry(QtCore.QRect(360, 130, 191, 71))
        self.label_login.setStyleSheet("font: 36pt \"Century Gothic\";\n"
"color: rgb(229, 232, 236);\n"
"")
        self.label_login.setAlignment(QtCore.Qt.AlignCenter)
        self.label_login.setObjectName("label_login")
        self.PasswordLine = QtWidgets.QLineEdit(Dialog)
        self.PasswordLine.setGeometry(QtCore.QRect(310, 410, 281, 41))
        self.PasswordLine.setStyleSheet("background-color:rgba(0,0,0,0);\n"
"font: 12pt \"Century Gothic\";")
        self.PasswordLine.setObjectName("PasswordLine")
        self.login_btn = QtWidgets.QPushButton(Dialog)
        self.login_btn.setGeometry(QtCore.QRect(330, 490, 231, 41))
        self.login_btn.setStyleSheet("border-radius:10px;\n"
"background-color: rgb(229, 232, 236);\n"
"\n"
"font: 14pt \"Century Gothic\";\n"
"")
        self.login_btn.setObjectName("login_btn")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(310, 290, 71, 31))
        self.label_3.setStyleSheet("font: 11pt \"Century Gothic\";")
        self.label_3.setObjectName("label_3")
        self.label_DSP = QtWidgets.QLabel(Dialog)
        self.label_DSP.setGeometry(QtCore.QRect(290, 210, 321, 50))
        self.label_DSP.setStyleSheet("font: 15pt \"Century Gothic\";\n"
"color: rgb(229, 232, 236);")
        self.label_DSP.setAlignment(QtCore.Qt.AlignCenter)
        self.label_DSP.setObjectName("label_DSP")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_4.setText(_translate("Dialog", "Password"))
        self.goback_btn.setText(_translate("Dialog", "Go back"))
        self.label_login.setText(_translate("Dialog", "Login"))
        self.login_btn.setText(_translate("Dialog", "Log In"))
        self.label_3.setText(_translate("Dialog", "Email"))
        self.label_DSP.setText(_translate("Dialog", "Disease Symptom Prediction"))
