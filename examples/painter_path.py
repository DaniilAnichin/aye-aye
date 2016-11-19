#!/usr/bin/python
# -*- coding: utf-8 -*- #
from PyQt4 import QtGui, QtCore
from elements.tools import Logger
logger = Logger()


class MyFrame(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(MyFrame, self).__init__(parent)

        scene = QtGui.QGraphicsScene(self)
        self.setScene(scene)

        # add some items
        r = 100
        x = 0
        y = 0
        w = 45
        h = 45
        pen = QtGui.QPen(QtGui.QColor(QtCore.Qt.green))
        brush = QtGui.QBrush(pen.color().darker(150))

        item = scene.addEllipse(r + x, r + y, w, h, pen, brush)
        item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

        # create an open path
        path = QtGui.QPainterPath()
        path.moveTo(r - w, r - h)
        path.lineTo(r - w, r + h)
        path.lineTo(r + w, r + h)
        path.lineTo(r + w, r - h)

        clr = QtGui.QColor('blue')
        clr.setAlpha(120)
        brush = QtGui.QBrush(clr)
        pen = QtGui.QPen(QtCore.Qt.NoPen)
        fill_item = scene.addRect(r - w, r + y, w * 2, h, pen, brush)
        path_item = scene.addPath(path)

    def mouseDoubleClickEvent(self, QMouseEvent):
        path = QtGui.QPainterPath()
        x = QMouseEvent.x()
        y = QMouseEvent.y()
        path.moveTo(100, 100)
        path.lineTo(x, y)
        self.scene().addPath(path)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    f = MyFrame()
    f.show()
    app.exec_()
