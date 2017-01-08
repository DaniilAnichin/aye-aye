#!/usr/bin/python
# -*- coding: utf-8 -*- #
from math import cos, sin, degrees, radians
from PyQt4 import QtGui, QtCore
from elements.Figure import Figure
from elements.tools import Logger, CountingTimer
import numpy as np
logger = Logger()


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


def similar(first, second):
    return QtCore.QLineF(first, second).length() < 15


def geronize(points):
    square = 0
    while len(points) >= 3:
        A = points[-1]
        B = points[-2]
        C = points[-3]
        AB = QtCore.QLineF(A, B).length()
        BC = QtCore.QLineF(B, C).length()
        AC = QtCore.QLineF(A, C).length()
        p = (AB + BC + AC) / 2
        square += (p * (p - AB) * (p - BC) * (p - AC)) ** 0.5
        points.pop()

    return square


def calculations(walls, window):
    points = [wall.line.p1() for wall in walls]
    coords = [[point.x(), point.y()] for point in points]
    angles = [walls[i].line.angleTo(walls[i-1].line) for i in range(len(walls))]
    true_angles = map(lambda x: x - 180, angles)
    # true_angles = angles
    center = np.mean(np.array(coords) / 5, axis=0).tolist()
    popup = QtGui.QMessageBox(window)
    popup.setIcon(QtGui.QMessageBox.Information)
    popup.setWindowTitle(u'Результаты')
    info_text = u"Количество сторон: {0}\n".format(len(walls))
    info_text += u"Длины сторон:\n"
    info_text += u", ".join(map(lambda wall: unicode(wall.line.length() / 5), walls))

    info_text += u"\nУглы:\n"
    info_text += u", ".join(map(unicode, true_angles))

    info_text += u"\nКоординаты точек: \n"
    info_text += u", ".join([
        u"({}, {})".format(*map(lambda x: x / 5, coord)) for coord in coords])
    info_text += u"\nКоординаты центра: \n"
    info_text += u"({}, {})".format(*center)

    info_text += u"\nПлощадь: \n"
    info_text += u"{}".format(geronize(points) / 25)

    popup.setText(info_text)
    popup.show()
