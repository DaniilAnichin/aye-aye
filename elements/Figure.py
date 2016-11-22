#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
from tools import Logger, invert
logger = Logger()
center_rad = 5


class Figure(QtGui.QWidget):
    default_color = QtGui.QColor('red')

    def __init__(self, parent=None, **kwargs):
        super(Figure, self).__init__(parent)
        self.scene = parent

    def update_params(self, **kwargs):
        self.color = kwargs.get('color')
