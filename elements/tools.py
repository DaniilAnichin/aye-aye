#!/usr/bin/python
# -*- coding: utf-8 -*- #
import threading
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
                os.path.join(BASE_DIR, u'aye-aye.log')
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


class CountingTimer(threading.Thread):
    def __init__(self, count, lapse, action):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.action = action
        self.count = count
        self.lapse = lapse

    def run(self):
        while self.count > 0 and not self.event.is_set():
            self.count -= 1
            self.event.wait(self.lapse)
            self.action()

    def stop(self):
        self.event.set()
