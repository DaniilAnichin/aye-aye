#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui


class Figure(object):
    default_color = QtGui.QColor('red')

    def __init__(self, parent=None, **kwargs):
        super(Figure, self).__init__()
        self.scene = parent
        self.points = kwargs.get('points', [])
        self.center = kwargs.get('center', [0, 0])
        self.color = kwargs.get('color', self.default_color)
