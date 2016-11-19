#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
from elements.Figure import Figure
from elements.tools import Logger, invert
logger = Logger()
center_rad = 5


class Bot(Figure):
    def __init__(self, parent=None, **kwargs):
        super(Bot, self).__init__(parent, **kwargs)
        self.update_params(**kwargs)
        self.direction = 0
        self.show()

    def update_params(self, **kwargs):
        logger.debug('Update called')
        self.width = 8 * kwargs.get('width')
        self.step = 8 * kwargs.get('step')
        self.color = kwargs.get('color')
        self.angle = kwargs.get('angle')
        self.time_step = 1000 * kwargs.get('time_step')
        self.setGeometry(100, 100, self.width, self.step)

    def perform_step(self, steps_number):
        pass

    def move_to(self, point):
        self.setGeometry(point.x(), point.y())

    def turn(self, angles_number):
        self.direction += int(angles_number * self.angle)

    def paintEvent(self, event):
        logger.debug('Bot is drawing')
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.rotate(45)
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        # make a white drawing background
        paint.setBrush(self.color)
        paint.drawRect(event.rect())

        paint.setPen(invert(self.color))
        paint.setBrush(self.color)
        paint.drawEllipse(self.pos(), *[center_rad] * 2)
