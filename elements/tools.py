#!/usr/bin/python
# -*- coding: utf-8 -*- #
import os
import logging
from PyQt4 import QtGui


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
README = os.path.join(BASE_DIR, 'README.md')


class Logger(logging.Logger):
    def __init__(self):
        super(Logger, self).__init__('root')
        if not self.level == logging.DEBUG:
            formatter = logging.Formatter(
    u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s'
            )

            filehandler = logging.FileHandler(
                os.path.join(BASE_DIR, u'easy_weeks.log')
            )
            filehandler.setFormatter(formatter)
            filehandler.setLevel(logging.INFO)
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            console.setLevel(logging.DEBUG)
            self.addHandler(filehandler)
            self.addHandler(console)


def invert(color):
    if not isinstance(color, QtGui.QColor):
        return

    consts = color.getRgb()
    new_consts = [255 - const for const in consts[:-1]] + [consts[-1]]

    return QtGui.QColor(*new_consts)
