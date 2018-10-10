# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'msg_window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(607, 427)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.friend_label = QtWidgets.QLabel(Form)
        self.friend_label.setObjectName("friend_label")
        self.gridLayout.addWidget(self.friend_label, 0, 0, 1, 1)
        self.msg_textBrowser = QtWidgets.QTextBrowser(Form)
        self.msg_textBrowser.setObjectName("msg_textBrowser")
        self.gridLayout.addWidget(self.msg_textBrowser, 1, 0, 1, 2)
        self.msg_textEdit = QtWidgets.QTextEdit(Form)
        self.msg_textEdit.setObjectName("msg_textEdit")
        self.gridLayout.addWidget(self.msg_textEdit, 2, 0, 1, 2)
        self.send_Button = QtWidgets.QPushButton(Form)
        self.send_Button.setObjectName("send_Button")
        self.gridLayout.addWidget(self.send_Button, 3, 0, 1, 1)
        self.recall_Button = QtWidgets.QPushButton(Form)
        self.recall_Button.setObjectName("recall_Button")
        self.gridLayout.addWidget(self.recall_Button, 3, 1, 1, 1)

        self.retranslateUi(Form)
        self.send_Button.clicked.connect(Form.send_func)
        self.recall_Button.clicked.connect(Form.recall_func)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.friend_label.setText(_translate("Form", "TextLabel"))
        self.send_Button.setText(_translate("Form", "Send"))
        self.recall_Button.setText(_translate("Form", "ReCall"))

