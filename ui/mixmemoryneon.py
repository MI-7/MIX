from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMdiSubWindow
from utility import *


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.memory = None

        # self.pen = QtGui.QPen(QtGui.QColor(0,0,0))                      # set lineColor
        # self.pen.setWidth(3)                                            # set lineWidth
        # self.brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))        # set fillColor
        # self.polygon = self.createPoly(8,150,0)                         # polygon with n points, radius, angle of the first point

        # def createPoly(self, n, r, s):
        # polygon = QtGui.QPolygonF()
        # w = 360/n                                                       # angle per step
        # for i in range(n):                                              # add the points of polygon
        # t = w*i + s
        # x = r*math.cos(math.radians(t))
        # y = r*math.sin(math.radians(t))
        # polygon.append(QtCore.QPointF(self.width()/2 +x, self.height()/2 + y))

        # return polygon

    def paintEvent(self, event):
        if self.memory is None:
            return

        startx, starty = 10, 10
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(0, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        red = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        green = QtGui.QBrush(QtGui.QColor(0, 255, 0))

        for i in range(80):
            for j in range(50):
                x = j * 80 + i
                m = self.memory.getMemory(x)
                if partstodec_withsign(m) == 0:
                    painter.setBrush(green)
                else:
                    painter.setBrush(red)
                painter.drawRect(i*10, j*10, 10, 10)


class MixMemoryNeon(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.mywidget = MyWidget()
        self.setWidget(self.mywidget)

    def refreshmemory(self, m):
        self.mywidget.memory = m
        self.mywidget.update()
