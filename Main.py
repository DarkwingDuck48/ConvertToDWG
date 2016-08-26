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
        self.setGeometry(400, 300, 250, 200)
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.file_win = None
        self.manual_win = None
        layout_grid = QtGui.QGridLayout()
        button_vbox = QtGui.QVBoxLayout()
        self.centralWidget.setLayout(layout_grid)

        icon_open = QtGui.QIcon("icons/note.png")
        menu_open = QtGui.QAction(icon_open, "Данные из файла", self)
        menu_open.setShortcut("Ctrl-O")
        menu_open.setStatusTip("Конвертация из файла")

        icon_exit = QtGui.QIcon("icons/power.png")
        menu_exit = QtGui.QAction(icon_exit, "Выход", self)
        menu_exit.setShortcut("Ctrl-Q")
        menu_open.setStatusTip("Выход")

        icon_manual = QtGui.QIcon("icons/pen.png")
        menu_manual = QtGui.QAction(icon_manual, "Создать новый", self)
        menu_manual.setShortcut("Ctrl-N")
        menu_manual.setStatusTip("Создание нового файла")

        # Сама панель
        self.menubar = self.menuBar()
        file = self.menubar.addMenu('&Файл')
        file.addAction(menu_manual)
        file.addAction(menu_open)
        file.addSeparator()
        file.addAction(menu_exit)

        button_file = QtGui.QPushButton("Чтение данных из файла",self.centralWidget)
        button_manual = QtGui.QPushButton("Введение данных вручную", self.centralWidget)
        button_exit = QtGui.QPushButton("Выход", self.centralWidget)

        button_vbox.addWidget(button_file)
        button_vbox.addWidget(button_manual)
        layout_grid.addLayout(button_vbox, 0, 1)
        layout_grid.addWidget(button_exit, 3, 1)

        self.connect(button_file, QtCore.SIGNAL('clicked()'), self.fromFile)
        self.connect(menu_open,QtCore.SIGNAL('triggered()'),self.fromFile)
        self.connect(button_manual, QtCore.SIGNAL('clicked()'),self.manual)
        self.connect(menu_manual, QtCore.SIGNAL('triggered()'), self.manual)
        self.connect(button_exit, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        self.connect(menu_exit,QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))

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
