#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
from elements.Figure import Figure
from elements.tools import Logger, CountingTimer
logger = Logger()
center_rad = 5


class Bot(Figure):
    # Params list:
    moved = True
    turned = False

    # move_angle = None
    last_nearest = None

    wall_size = 2.5
    wall_angle = None
    temp_ray = None
    ray = None

    destination = None
    center = None
    direction = 0

    radius = 1
    step = 1
    color = None
    ray_color = None
    time_step = .01
    angle = 1
    timer = None
    move_number = 0

    def __init__(self, parent=None, **kwargs):
        super(Bot, self).__init__(parent, **kwargs)
        self.center = QtCore.QPointF(0, 0)
        self.block_center = False
        self.update_params(**kwargs)
        self.move(0, 0)
        self.show()

    def update_params(self, **kwargs):
        self.setGeometry(self.parent().rect())
        for key in kwargs.keys():
            if not (key == 'center' and self.block_center):
                setattr(self, key, kwargs[key])

        self.block_center = True
        self.update()

    def go_home(self, **kwargs):
        self.block_center = False
        self.update_params(**kwargs)

    def suites(self, direction_ray):
        angles = [-90, -45, 0, 45, 90]
        intersections = []
        for angle in angles:
            radial = QtCore.QLineF()
            radial.setP1(self.center)
            radial.setAngle(direction_ray.angle() + angle)
            radial.setLength(self.radius)
            guide = QtCore.QLineF()
            guide.setP1(radial.p2())
            guide.setAngle(direction_ray.angle())
            guide.setLength(direction_ray.length())
            intersections += self.intersections(guide)
        return True if not intersections else False

    def step_ray(self):
        temp_line = QtCore.QLineF()
        temp_line.setP1(self.center)
        temp_line.setAngle(self.direction)
        temp_line.setLength(self.step)
        return temp_line

    def destination_ray(self):
        return QtCore.QLineF(self.center, self.destination)

    def perform_step(self):
        # Set params if starting algorithm
        # if self.move_number > 50:
        #     self.angle = -self.angle
        #     self.move_number = 0

        if self.suites(self.destination_ray()):
            if self.destination_ray().length() < self.step:
                self.timer.stop()
                self.wall_angle = None
                return
            self.direction = self.destination_ray().angle()
            self.center = self.step_ray().p2()
            self.move_number += 1
            self.update()
            return

        if not self.wall_angle:
            # if self.moved:
            self.direction = self.destination_ray().angle()
            self.temp_ray = self.step_ray()
            if self.suites(self.temp_ray):
                self.center = self.step_ray().p2()
                self.moved = True
            else:
                self.wall_angle = self.direction
            self.update()
            return

        self.temp_ray = self.step_ray()
        if self.turned:
            if self.suites(self.temp_ray):
                self.center = self.temp_ray.p2()
                self.move_number += 1
                self.turned = False
                self.moved = True
            else:
                self.direction -= self.angle
        else:
            if self.suites(self.temp_ray):
                self.direction += self.angle
            else:
                self.turned = True
                self.direction -= self.angle

        self.update()

    def move_to_aim(self):
        self.move_number = 0
        self.timer = CountingTimer(
            10 ** 6, self.time_step, self.perform_step
        )
        self.timer.start()

    def perform_turn(self):
        self.update()
        if self.intersections(self.ray):
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

    def intersections(self, ray):
        intersections = []
        for line in [wall.line for wall in self.parent().walls]:
            dot = QtCore.QPointF()
            if ray.intersect(line, dot) == QtCore.QLineF.BoundedIntersection:
                intersections.append(dot)
        return intersections

    def nearest(self, ray):
        lines = [
            QtCore.QLineF(self.center, intersect)
            for intersect in self.intersections(ray)
        ]
        if not lines:
            return None
        lines.sort(key=lambda a: a.length())
        return lines[0]

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
        paint.drawLine(self.step_ray())

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
        for intersect in self.intersections(self.ray):
            paint.drawPoint(intersect)

    def draw_aim(self, paint):
        paint.setPen(QtGui.QPen(
            self.ray_color.darker(), 14,
            QtCore.Qt.SolidLine, QtCore.Qt.RoundCap
        ))
        if self.destination:
            paint.drawPoint(self.destination)
