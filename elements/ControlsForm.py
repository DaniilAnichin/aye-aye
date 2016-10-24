#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
from translate import fromUtf8

class ControlsForm(QtGui.QFormLayout):
    def __init__(self, *args):
        super(ControlsForm, self).__init__(*args)

        self.label = QtGui.QLabel()
        self.label_2 = QtGui.QLabel()
        self.label_3 = QtGui.QLabel()
        self.label_4 = QtGui.QLabel()
        self.doubleSpinBox = QtGui.QDoubleSpinBox()
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox()
        self.spinBox = QtGui.QSpinBox()
        self.spinBox_2 = QtGui.QSpinBox()

        self.pushButton = QtGui.QPushButton()
        self.pushButton_2 = QtGui.QPushButton()
        self.pushButton_3 = QtGui.QPushButton()
        self.pushButton_4 = QtGui.QPushButton()
        self.pushButton_5 = QtGui.QPushButton()
        self.pushButton_6 = QtGui.QPushButton()
        self.pushButton_7 = QtGui.QPushButton()
        self.pushButton_8 = QtGui.QPushButton()

        self.addRow(self.label, self.spinBox_2)
        self.addRow(self.label_2, self.doubleSpinBox)
        self.addRow(self.label_3, self.spinBox)
        self.addRow(self.label_4, self.doubleSpinBox_2)

        self.addRow(self.pushButton, self.pushButton_2)
        self.addRow(self.pushButton_3, self.pushButton_4)

        self.setWidget(6, QtGui.QFormLayout.SpanningRole, self.pushButton_5)
        self.setWidget(7, QtGui.QFormLayout.SpanningRole, self.pushButton_7)
        self.setWidget(8, QtGui.QFormLayout.SpanningRole, self.pushButton_6)
        self.setWidget(9, QtGui.QFormLayout.SpanningRole, self.pushButton_8)

        self.retranslateUi()

    def retranslateUi(self):
        self.label.setText(fromUtf8('TextLabel'))
        self.label_2.setText(fromUtf8('TextLabel'))
        self.label_4.setText(fromUtf8('TextLabel'))
        self.label_3.setText(fromUtf8('TextLabel'))
        self.pushButton_2.setText(fromUtf8('PushButton'))
        self.pushButton.setText(fromUtf8('PushButton'))
        self.pushButton_4.setText(fromUtf8('PushButton'))
        self.pushButton_3.setText(fromUtf8('PushButton'))
        self.pushButton_5.setText(fromUtf8('PushButton'))
        self.pushButton_7.setText(fromUtf8('PushButton'))
        self.pushButton_6.setText(fromUtf8('PushButton'))
        self.pushButton_8.setText(fromUtf8('PushButton'))


def main():
    pass

if __name__ == "__main__":
    main()
