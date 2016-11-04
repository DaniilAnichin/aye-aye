#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui


def invert(color):
    if not isinstance(color, QtGui.QColor):
        return

    consts = color.getRgb()
    new_consts = [255 - const for const in consts[:-1]] + [consts[-1]]

    return QtGui.QColor(*new_consts)
