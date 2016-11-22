#!/usr/bin/python
# -*- coding: utf-8 -*- #
from math import cos, sin, degrees, radians
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
        self.center = QtCore.QPointF(0, 0)
        self.block_center = False
        self.update_params(**kwargs)
        self.move(0, 0)
        self.show()

    def update_params(self, **kwargs):
        # logger.debug('Update called')
        self.setGeometry(self.parent().rect())
        self.radius = 5 * kwargs.get('width')
        self.step = 5 * kwargs.get('step')
        self.color = kwargs.get('color')
        self.angle = kwargs.get('angle')
        self.time_step = kwargs.get('time_step') / 100.
        self.direction = kwargs.get('direction')
        if not self.block_center:
            self.center = QtCore.QPointF(5 * kwargs.get('x'), 5 * kwargs.get('y'))
        self.block_center = True
        self.update()

    def go_home(self, **kwargs):
        self.block_center = False
        self.update_params(**kwargs)

    def perform_step(self):
        x = self.center.x() + self.step * cos(radians(self.direction))
        y = self.center.y() + self.step * sin(radians(self.direction))
        self.center.setX(x)
        self.center.setY(y)
        self.update()

    def move_to(self, point):
        self.setGeometry(point.x(), point.y())

    def perform_turn(self):
        self.direction = (self.direction + self.angle) % 360
        self.turn_number += 1
        self.update()

    def turn(self, angle):
        # logger.debug('Called')
        if angle > 3600:
            return
        self.timer = CountingTimer(angle / self.angle, self.time_step, self.perform_turn)
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
