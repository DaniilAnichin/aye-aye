#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
from elements.Bot import Bot, Figure


class Scene(QtGui.QWidget):
    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args)
        self.bot = Bot(self, **kwargs)
        self.setSizePolicy(QtGui.QSizePolicy(*[QtGui.QSizePolicy.Expanding] * 2))
        self.setWindowTitle('Draw circles')

    def paintEvent(self, event):
        for child in self.children():
            if isinstance(child, Figure):
                self.draw_figure(child)

        paint = QtGui.QPainter()
        paint.begin(self)
        # optional
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(QtGui.QColor('white'))
        paint.drawRect(event.rect())
        # for circle make the ellipse radii match
        radx = 100
        rady = 100
        # draw red circles
        paint.setPen(QtGui.QColor('red'))
        paint.setBrush(QtGui.QColor('yellow'))
        for k in range(125, 220, 10):
            center = QtCore.QPoint(k, k)
            # optionally fill each circle yellow
            paint.drawEllipse(center, radx, rady)
        paint.end()

    def draw_figure(self):
        pass
