# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat_client_ui.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(799, 592)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ChatText = QtWidgets.QTextBrowser(self.centralwidget)
        self.ChatText.setGeometry(QtCore.QRect(180, 30, 601, 441))
        self.ChatText.setObjectName("ChatText")
        self.TextEingabe = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.TextEingabe.setGeometry(QtCore.QRect(180, 470, 541, 61))
        self.TextEingabe.setObjectName("TextEingabe")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(110, 0, 61, 16))
        self.label.setObjectName("label")
        self.SendButton = QtWidgets.QPushButton(self.centralwidget)
        self.SendButton.setGeometry(QtCore.QRect(720, 470, 61, 31))
        self.SendButton.setObjectName("SendButton")
        self.UserList = QtWidgets.QListView(self.centralwidget)
        self.UserList.setGeometry(QtCore.QRect(20, 150, 141, 192))
        self.UserList.setObjectName("UserList")
        self.toggleLocalHost = QtWidgets.QCheckBox(self.centralwidget)
        self.toggleLocalHost.setGeometry(QtCore.QRect(710, 0, 81, 20))
        self.toggleLocalHost.setObjectName("toggleLocalHost")
        self.ConnectButton = QtWidgets.QPushButton(self.centralwidget)
        self.ConnectButton.setGeometry(QtCore.QRect(10, 0, 93, 28))
        self.ConnectButton.setObjectName("ConnectButton")
        self.ServerIPLine = QtWidgets.QLineEdit(self.centralwidget)
        self.ServerIPLine.setGeometry(QtCore.QRect(170, 0, 221, 22))
        self.ServerIPLine.setText("")
        self.ServerIPLine.setObjectName("ServerIPLine")
        self.AliasLine = QtWidgets.QLineEdit(self.centralwidget)
        self.AliasLine.setGeometry(QtCore.QRect(622, 0, 71, 22))
        self.AliasLine.setObjectName("AliasLine")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(580, 0, 31, 16))
        self.label_2.setObjectName("label_2")
        self.PortLine = QtWidgets.QLineEdit(self.centralwidget)
        self.PortLine.setGeometry(QtCore.QRect(436, 0, 113, 22))
        self.PortLine.setObjectName("PortLine")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(400, 0, 31, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 130, 101, 16))
        self.label_4.setObjectName("label_4")
        self.HelpButton = QtWidgets.QPushButton(self.centralwidget)
        self.HelpButton.setGeometry(QtCore.QRect(720, 500, 61, 28))
        self.HelpButton.setObjectName("HelpButton")
        self.DisconnectButton = QtWidgets.QPushButton(self.centralwidget)
        self.DisconnectButton.setGeometry(QtCore.QRect(10, 30, 93, 28))
        self.DisconnectButton.setObjectName("DisconnectButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 799, 26))
        self.menubar.setObjectName("menubar")
        self.menuChat = QtWidgets.QMenu(self.menubar)
        self.menuChat.setObjectName("menuChat")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuChat.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TextEingabe.setPlainText(_translate("MainWindow", "type here"))
        self.label.setText(_translate("MainWindow", "Server IP:"))
        self.SendButton.setText(_translate("MainWindow", "send"))
        self.toggleLocalHost.setText(_translate("MainWindow", "local host"))
        self.ConnectButton.setText(_translate("MainWindow", "connect"))
        self.AliasLine.setText(_translate("MainWindow", "anon"))
        self.label_2.setText(_translate("MainWindow", "Alias:"))
        self.label_3.setText(_translate("MainWindow", "Port:"))
        self.label_4.setText(_translate("MainWindow", "currently online:"))
        self.HelpButton.setText(_translate("MainWindow", "help"))
        self.DisconnectButton.setText(_translate("MainWindow", "disconnect"))
        self.menuChat.setTitle(_translate("MainWindow", "Chat"))

