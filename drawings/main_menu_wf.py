#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
from PyQt4 import QtCore, QtGui
from elements.ControlsForm import ControlsForm
from translate import fromUtf8


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(824, 601)
        self.center = QtGui.QWidget()

        self.hbox = QtGui.QHBoxLayout(self.center)
        self.graphicsView = QtGui.QGraphicsView(self)
        self.hbox.addWidget(self.graphicsView)
        self.controls_form = ControlsForm(self)
        self.hbox.addLayout(self.controls_form)

        self.setCentralWidget(self.center)

        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 824, 19))
        self.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(self)
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        self.setWindowTitle(fromUtf8('Окно'))


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
