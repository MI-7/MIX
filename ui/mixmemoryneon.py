import math, sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMdiSubWindow


class MyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.pen = QtGui.QPen(QtGui.QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                            # set lineWidth
        self.brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))        # set fillColor
        self.polygon = self.createPoly(8,150,0)                         # polygon with n points, radius, angle of the first point

    def createPoly(self, n, r, s):
        polygon = QtGui.QPolygonF()
        w = 360/n                                                       # angle per step
        for i in range(n):                                              # add the points of polygon
            t = w*i + s
            x = r*math.cos(math.radians(t))
            y = r*math.sin(math.radians(t))
            polygon.append(QtCore.QPointF(self.width()/2 +x, self.height()/2 + y))

        return polygon

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(self.polygon)


class MixMemoryNeon(QMdiSubWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mywidget = MyWidget()
        self.setWidget(mywidget)
