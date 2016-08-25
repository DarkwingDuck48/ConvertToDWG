"""
Maxim Britvin, 2016
email: maksbritvin@gmail.com
"""

import sys

from PyQt4 import QtGui, QtCore
from ConvertDXF import Window
from ManualConvert import Manual


class Core(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Core, self).__init__(parent)

        # Настройка главного окна
        self.setGeometry(400, 300, 100, 200)
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.file_win = None
        self.manual_win = None
        layout_grid = QtGui.QGridLayout()
        vbox = QtGui.QVBoxLayout()
        self.centralWidget.setLayout(layout_grid)

        button_file = QtGui.QPushButton("Чтение данных из файла",self.centralWidget)
        button_manual = QtGui.QPushButton("Введение данных вручную", self.centralWidget)

        vbox.addWidget(button_file)
        vbox.addWidget(button_manual)
        layout_grid.addLayout(vbox,0,1)

        self.connect(button_file, QtCore.SIGNAL('clicked()'), self.fromFile)
        self.connect(button_manual, QtCore.SIGNAL('clicked()'),self.manual)

    def fromFile(self):
        if not self.file_win:
            self.file_win = Window(self)
        self.file_win.show()

    def manual(self):
        if not self.manual_win:
            self.manual_win = Manual(self)
        self.manual_win.show()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Core()
    window.show()
    sys.exit(app.exec_())
