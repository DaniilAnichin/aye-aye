#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
from elements.Bot import Bot
from elements.Wall import Wall
from elements.tools import Logger
logger = Logger()


class Scene(QtGui.QFrame):
    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args)
        self.setSizePolicy(QtGui.QSizePolicy(*[QtGui.QSizePolicy.Expanding] * 2))
        self.update_color(**kwargs)
        self.walls = []
        self.draw_rulers()

    def update_color(self, color=None, staff_color=None):
        self.color = color
        self.wall_color = staff_color
        self.setStyleSheet('''
            background-color: %s;
            border: 1px solid #8f8f91;
            ''' % self.color.name()
        )

    def create_bot(self, **kwargs):
        self.bot = Bot(self, **kwargs)

    def update_bot(self, **kwargs):
        self.bot.update_params(**kwargs)

    def reset(self, **kwargs):
        for wall in self.walls:
            self.walls.remove(wall)
            wall.deleteLater()
        self.bot.go_home(**kwargs)
        self.update()

    # Drawing lines
    def mousePressEvent(self, event):
        self.start = event.posF()

    def mouseReleaseEvent(self, event):
        self.end = event.posF()
        line = QtCore.QLineF(self.start, self.end)
        wall = Wall(line, self, self.wall_color)
        wall.show()
        self.walls.append(wall)
        self.bot.update()

    def draw_rulers(self):
        # TODO draw rulers on the sides of the scene
        pass
