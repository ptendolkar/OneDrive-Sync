# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/Pleb/Documents/Qt/onedrivesync.ui'
#
# Created: Wed Jun 24 22:16:13 2015
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 100)
        self.tokenButton = QtGui.QPushButton(Dialog)
        self.tokenButton.setGeometry(QtCore.QRect(66, 50, 87, 31))
        self.tokenButton.setObjectName("tokenButton")
        self.quitButton = QtGui.QPushButton(Dialog)
        self.quitButton.setGeometry(QtCore.QRect(250, 50, 85, 31))
        self.quitButton.setObjectName("quitButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "OneDrive Sync", None, QtGui.QApplication.UnicodeUTF8))
        self.tokenButton.setText(QtGui.QApplication.translate("Dialog", "Get Token", None, QtGui.QApplication.UnicodeUTF8))
        self.quitButton.setText(QtGui.QApplication.translate("Dialog", "Quit", None, QtGui.QApplication.UnicodeUTF8))

