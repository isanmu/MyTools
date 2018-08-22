#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 7/4/2018 10:19
# @Author  : Winson
# @User    : winswang
# @Site    : 
# @File    : main_tools.py
# @Project : MyTools
# @Software: PyCharm

import sys
import traceback

import pyperclip
from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, qApp

from ui_files.mytools_gui import Ui_MainWindow
from Tool_1 import init_var_list, self_var_list, star_unordered_list


class MyMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def to_list(self):
        try:
            num = self.var_numer_of_line.value()
            init_var_list(num)
            print('Done: to_list(%s)!' % num)
        except Exception as e:
            show_mainwindow_error(self, e)

    def to_self_equal(self):
        try:
            self_var_list()
            print('Done: to_self_equal !')
        except Exception as e:
            show_mainwindow_error(self, e)

    def text_symbol(self):
        try:
            symbol = self.symbolBox.currentText()
            # print(repr(symbol))
            plus = 1 if self.plusBox.currentText() == '+' else 0
            print('plus = ', plus)
            direct = self.directBox.currentText()
            # assert str(direct) is 'all'
            if direct == 'left':
                direct = 1
            elif direct == 'all':
                direct = 2
            elif direct == 'right':
                direct = 0
            print('direct = ', direct)
            new_text = star_unordered_list(str(symbol), plus=plus, direct=direct)
            print('Done: add_nonorder_symbol !')
            print('Result:', new_text)
        except Exception as e:
            traceback.print_exc()
            show_mainwindow_error(self, e)

    def add_copy(self):
        text = self.copytext.toPlainText()
        pyperclip.copy(text)


def show_mainwindow_error(win, error):
    QMessageBox.information(win, "Error", str(error) + '\n', QMessageBox.Ok)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mywindow = MyMainWindow()
    mywindow.show()
    sys.exit(app.exec_())
