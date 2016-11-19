#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
from elements.Bot import Bot
from elements.tools import Logger
logger = Logger()


stylesheet = '''
    background-color: %s;
    border: 1px solid #8f8f91;
'''


class Scene(QtGui.QFrame):
    def __init__(self, *args, **kwargs):
        super(Scene, self).__init__(*args)
        self.setSizePolicy(QtGui.QSizePolicy(*[QtGui.QSizePolicy.Expanding] * 2))
        self.update_color(**kwargs)
        self.draw_rulers()

    def update_color(self, **kwargs):
        self.color = kwargs.get('color')
        self.setStyleSheet(stylesheet % self.color.name())

    def create_bot(self, **kwargs):
        self.bot = Bot(self, **kwargs)

    def update_bot(self, **kwargs):
        self.bot.update_params(**kwargs)

    def draw_rulers(self):
        # TODO draw rulers on the sides of the scene
        pass
