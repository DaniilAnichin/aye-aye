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
        self.destination = None
        self.ray = None
        self.step_ray = None
        self.intersects = []
        self.direction = 0
        self.turn_number = 0
        self.center = QtCore.QPointF(0, 0)
        self.block_center = False
        self.update_params(**kwargs)
        self.move(0, 0)
        self.show()

    def update_params(self, **kwargs):
        self.setGeometry(self.parent().rect())
        self.radius = 5 * kwargs.get('width')
        self.step = 5 * kwargs.get('step')
        self.color = kwargs.get('color')
        self.ray_color = kwargs.get('ray_color')
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
        self.direction = (self.direction + self.angle) % 360
        self.turn_number += 1
        x = self.center.x() + self.step * cos(radians(self.direction))
        y = self.center.y() + self.step * sin(radians(self.direction))
        dest = QtCore.QPointF(x, y)
        self.ray = QtCore.QLineF(self.center, dest)
        if self.intersects:
            self.timer.stop()
            return
        else:
            self.center = dest

        self.update()

    def move_to_aim(self):
        self.timer = CountingTimer(
            10 ** 6, self.time_step, self.perform_step
        )
        self.timer.start()

    def perform_turn(self):
        self.update()
        if self.intersects:
            self.timer.stop()
            return
        self.direction = (self.direction + self.angle) % 360
        self.turn_number += 1

    def turn(self, angle):
        if angle > 3600:
            return
        self.timer = CountingTimer(
            abs(angle / self.angle), self.time_step, self.perform_turn
        )
        self.timer.start()

    def update_ray(self):
        self.ray = QtCore.QLineF(
            self.center.x(),
            self.center.y(),
            self.center.x() + 1000 * cos(radians(self.direction)),
            self.center.y() + 1000 * sin(radians(self.direction))
        )
        self.intersects = []
        for line in [wall.line for wall in self.parent().walls]:
            dot = QtCore.QPointF()
            if self.ray.intersect(line, dot) == QtCore.QLineF.BoundedIntersection:
                self.intersects.append(dot)

    # Drawing starts here
    def paintEvent(self, event):
        self.update_ray()

        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setRenderHint(QtGui.QPainter.Antialiasing)

        paint.translate(self.center)
        paint.rotate(self.direction)
        self.draw_step(paint)
        self.draw_ray(paint)
        self.draw_self(paint)

        paint.rotate(-self.direction)
        paint.translate(-self.center)
        self.draw_dots(paint)
        self.draw_aim(paint)

    def draw_step(self, paint):
        paint.setPen(self.color.lighter(150))
        paint.setBrush(self.color.lighter(150))
        paint.drawEllipse(
            self.step - self.radius,
            -self.radius,
            2 * self.radius,
            2 * self.radius
        )
        paint.drawRect(0, -self.radius, self.step, 2 * self.radius)

    def draw_self(self, paint):
        paint.setPen(self.color)
        paint.setBrush(self.color)
        paint.drawEllipse(
            -self.radius, -self.radius,
            2 * self.radius, 2 * self.radius
        )

    def draw_ray(self, paint):
        paint.setPen(QtGui.QPen(self.ray_color, 5))
        paint.drawLine(0, 0, 1000, 0)

    def draw_dots(self, paint):
        paint.setPen(QtGui.QPen(
            self.ray_color.darker(), 14,
            QtCore.Qt.SolidLine, QtCore.Qt.RoundCap
        ))
        for intersect in self.intersects:
            paint.drawPoint(intersect)

    def draw_aim(self, paint):
        paint.setPen(QtGui.QPen(
            self.ray_color.darker(), 14,
            QtCore.Qt.SolidLine, QtCore.Qt.RoundCap
        ))
        if self.destination:
            paint.drawPoint(self.destination)


