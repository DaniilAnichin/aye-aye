#!/usr/bin/python
# -*- coding: utf-8 -*- #
from math import cos, sin, degrees, radians
from PyQt4 import QtGui, QtCore
from elements.Figure import Figure
from elements.tools import Logger, CountingTimer
logger = Logger()
center_rad = 5


class Wall(Figure):
    def __init__(self, line, parent=None, color=None):
        super(Wall, self).__init__(parent)
        self.color = color
        self.line = line
        self.setGeometry(self.parent().rect())

    # Drawing starts here
    def paintEvent(self, event):
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setRenderHint(QtGui.QPainter.Antialiasing)

        paint.setPen(QtGui.QPen(self.color, 5))
        paint.drawLine(self.line)
