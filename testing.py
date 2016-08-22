import ezdxf
import os, sys
from PyQt4 import QtGui, QtCore

class Window(QtGui.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setGeometry(300, 300, 280, 270)

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()

    def drawPoints(self, qp):
        pen = QtGui.QPen(QtCore.Qt.SolidLine)
        qp.setPen(pen)
        dxf = ezdxf.readfile("testFiles\\так.dxf")
        msp = dxf.modelspace()
        points = []
        for point in list(msp.query('LWPOLYLINE')[0]):
            x = [point[0], point[1]]
            points.append(x)
        print(points)

        draw_points = []
        for i in points:
            x = int(i[0])
            y = int(i[1])
            qpoint = QtCore.QPoint(x,y)
            draw_points.append(qpoint)
        print(draw_points)

        i = 0
        qp.drawPolyline(*draw_points)



app = QtGui.QApplication(sys.argv)
ex = Window()
ex.show()
sys.exit(app.exec_())