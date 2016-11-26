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
        self.turned = False
        self.moved = False

        self.destination = None
        self.ray = None
        self.direction = 0
        self.turn_number = 0
        self.center = QtCore.QPointF(0, 0)
        self.block_center = False
        self.update_params(**kwargs)
        self.move(0, 0)
        self.show()

    def update_params(self, **kwargs):
        self.setGeometry(self.parent().rect())
        if not self.block_center:
            self.center = QtCore.QPointF(5 * kwargs.get('x'), 5 * kwargs.get('y'))

        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

        self.block_center = True
        self.update()

    def go_home(self, **kwargs):
        self.block_center = False
        self.update_params(**kwargs)

    def step_dest(self):
        temp_line = QtCore.QLineF()
        temp_line.setP1(self.center)
        temp_line.setAngle(self.direction)
        temp_line.setLength(self.step)
        return temp_line.p2()

    def perform_step(self):
        temp_ray = QtCore.QLineF(self.center, self.destination)
        if not self.moved:
            self.direction = temp_ray.angle()
            self.moved = True
        self.ray = QtCore.QLineF(self.center, self.step_dest())

        if temp_ray.length() < self.step:
            self.moved = False
            self.timer.stop()
            return

        if self.intersections():
            if not self.turned and abs(self.ray.angle()) > 135:
                self.turned = True
                self.angle = -self.angle
            else:
                self.direction += self.angle
        else:
            self.ray = temp_ray
            if not self.intersections():
                self.moved = False
            self.center = self.ray.p2()
            self.turn_number += 1
        self.update()

    def move_to_aim(self):
        self.turn_number = 0
        self.timer = CountingTimer(
            10 ** 6, self.time_step, self.perform_step
        )
        self.timer.start()

    def perform_turn(self):
        self.update()
        if self.intersections():
            self.timer.stop()
            return
        self.direction = (self.direction + self.angle) % 360

    def turn(self, angle):
        if angle > 3600:
            return
        self.timer = CountingTimer(
            abs(angle / self.angle), self.time_step, self.perform_turn
        )
        self.timer.start()

    def update_ray(self):
        self.ray = QtCore.QLineF()
        self.ray.setP1(self.center)
        self.ray.setAngle(self.direction)
        self.ray.setLength(1000)

    def intersections(self):
        intersections = []
        for line in [wall.line for wall in self.parent().walls]:
            dot = QtCore.QPointF()
            if self.ray.intersect(line, dot) == QtCore.QLineF.BoundedIntersection:
                intersections.append(dot)
        return intersections

    def nearest(self):
        lines = [QtCore.QLineF(self.center, intersect) for intersect in self.intersections()]
        lines.sort(key=lambda a: a.length())
        return lines[:1]

    # Drawing starts here
    def paintEvent(self, event):
        self.update_ray()

        paint = QtGui.QPainter()
        paint.begin(self)
        paint.setRenderHint(QtGui.QPainter.Antialiasing)

        self.draw_step(paint)
        self.draw_ray(paint)
        self.draw_self(paint)
        self.draw_dots(paint)
        self.draw_aim(paint)

    def draw_step(self, paint):
        paint.setPen(QtGui.QPen(
            self.color.lighter(), self.radius * 2,
            QtCore.Qt.SolidLine, QtCore.Qt.RoundCap
        ))
        paint.setBrush(self.color.lighter(150))
        paint.drawLine(self.center, self.step_dest())

    def draw_self(self, paint):
        paint.setPen(QtGui.QPen(
            self.color, self.radius * 2,
            QtCore.Qt.SolidLine, QtCore.Qt.RoundCap
        ))
        paint.drawPoint(self.center)

    def draw_ray(self, paint):
        paint.setPen(QtGui.QPen(self.ray_color, 5))
        paint.drawLine(self.ray)

    def draw_dots(self, paint):
        paint.setPen(QtGui.QPen(
            self.ray_color.darker(), 14,
            QtCore.Qt.SolidLine, QtCore.Qt.RoundCap
        ))
        for intersect in self.intersections():
            paint.drawPoint(intersect)

    def draw_aim(self, paint):
        paint.setPen(QtGui.QPen(
            self.ray_color.darker(), 14,
            QtCore.Qt.SolidLine, QtCore.Qt.RoundCap
        ))
        if self.destination:
            paint.drawPoint(self.destination)
