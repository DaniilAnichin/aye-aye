#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
from elements.Figure import Figure


class Bot(Figure):
    def __init__(self, parent=None, **kwargs):
        super(Bot, self).__init__(parent, **kwargs)
