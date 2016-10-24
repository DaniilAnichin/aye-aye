#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtCore


try:
    fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def fromUtf8(s):
        return s
