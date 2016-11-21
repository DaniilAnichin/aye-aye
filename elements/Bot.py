#!/usr/bin/python
# -*- coding: utf-8 -*- #
# from math import cos, sin, degrees, radians
from PyQt4 import QtGui, QtCore
from elements.Figure import Figure
from elements.tools import Logger, CountingTimer
logger = Logger()
center_rad = 5


class Bot(Figure):
    def __init__(self, parent=None, **kwargs):
        super(Bot, self).__init__(parent, **kwargs)

        self.direction = 0
        self.turn_number = 0
        self.center = QtCore.QPoint(0, 0)
        self.update_params(**kwargs)

        self.resize(self.parent().size())
        self.show()

    def update_params(self, **kwargs):
        # logger.debug('Update called')
        self.radius = 5 * kwargs.get('width')
        self.step = 5 * kwargs.get('step')
        self.color = kwargs.get('color')
        self.angle = kwargs.get('angle')
        self.time_step = kwargs.get('time_step') / 100.
        self.direction = kwargs.get('direction')
        self.center = QtCore.QPoint(5 * kwargs.get('x'), 5 * kwargs.get('y'))

    def perform_step(self, steps_number):
        pass

    def move_to(self, point):
        self.setGeometry(point.x(), point.y())

    def turn(self):
        self.direction = (self.direction + self.angle) % 360
        self.turn_number += 1
        self.update()

    def full_turn(self):
        logger.debug('Called')
        self.timer = CountingTimer(360 / self.angle, self.time_step, self.turn)
        self.timer.start()

    # Drawing starts here
    def paintEvent(self, event):
        # logger.debug('Bot is drawing')
        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.translate(self.center)
        paint.rotate(self.direction)

        paint.setPen(self.color.lighter(150))
        paint.setBrush(self.color.lighter(150))
        paint.drawEllipse(*self.step_ellipse_params())
        paint.drawRect(*self.step_rect_params())

        paint.setPen(self.color)
        paint.setBrush(self.color)
        paint.drawEllipse(*self.draw_params())

    def step_ellipse_params(self):
        return [
            self.step - self.radius,
            -self.radius,
            2 * self.radius,
            2 * self.radius
        ]

    def step_rect_params(self):
        return [0, -self.radius, self.step, 2 * self.radius]

    def draw_params(self):
        return [-self.radius, -self.radius, 2 * self.radius, 2 * self.radius]
