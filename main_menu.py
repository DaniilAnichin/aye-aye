#!/usr/bin/python
# -*- coding: utf-8 -*- #
import sys
# from functools import partial
from PyQt4 import QtCore, QtGui
from elements.ControlsForm import ControlsForm
from elements.Scene import Scene
from translate import fromUtf8
from elements.tools import Logger
logger = Logger()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(800, 600)
        self.setCentralWidget(QtGui.QWidget())
        self.hbox = QtGui.QHBoxLayout(self.centralWidget())

        self.controls = ControlsForm()
        self.scene = Scene(color=self.controls.scene_color)
        self.scene.create_bot(**self.controls.bot_params())
        self.controls.edited.connect(
            lambda: self.scene.update_bot(**self.controls.bot_params())
        )
        self.controls.edited.connect(
            lambda: self.scene.update_color(color=self.controls.scene_color)
        )
        self.hbox.addWidget(self.scene)
        self.hbox.addLayout(self.controls)

        self.setMenuBar(QtGui.QMenuBar(self))
        self.setStatusBar(QtGui.QStatusBar(self))

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
