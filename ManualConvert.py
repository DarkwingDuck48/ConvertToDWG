"""
Maxim Britvin, 2016
email: maksbritvin@gmail.com
"""

import os
import sys

from PyQt4 import QtGui, QtCore


class Manual(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Manual, self).__init__(parent)

        # Настройка главного окна
        self.setGeometry(400, 300, 280, 400)
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Manual()
    window.show()
    sys.exit(app.exec_())