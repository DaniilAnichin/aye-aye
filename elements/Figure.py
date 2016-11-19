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
        # self.points = kwargs.get('points', [])
        if not kwargs.get('color'):
            kwargs.update({'color': self.default_color})
        self.update_params(**kwargs)
        self.show()

    def update_params(self, **kwargs):
        self.color = kwargs.get('color')

    def paintEvent(self, event):
        logger.debug('Something is still happen')
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(QtGui.QColor('black'))
        paint.drawRect(event.rect())

        paint.setPen(invert(self.color))
        paint.setBrush(self.color)
        paint.drawEllipse(self.center, *[center_rad] * 2)
        for point in self.points:
            paint.drawEllipse(point, 10, 10)
