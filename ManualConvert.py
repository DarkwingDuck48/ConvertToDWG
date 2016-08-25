"""
Maxim Britvin, 2016
email: maksbritvin@gmail.com

TODO:
В момент нажатия кнопки OK - открывается окно выбора места сохранения файла.
"""

import os
import sys

from PyQt4 import QtGui, QtCore


class Manual(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Manual, self).__init__(parent)

        # Настройка главного окна
        self.setGeometry(400, 300, 361, 454)
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)

        layout_grid = QtGui.QGridLayout()
        layout_vbox = QtGui.QVBoxLayout()
        layout_text_edit = QtGui.QHBoxLayout()
        layout_radio = QtGui.QHBoxLayout()
        layout_buttons = QtGui.QHBoxLayout()
        layout_grid.addLayout(layout_vbox, 0, 0)
        self.centralWidget.setLayout(layout_grid)

        self.table = QtGui.QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderItem(0, QtGui.QTableWidgetItem("Координата X"))
        self.table.setHorizontalHeaderItem(1, QtGui.QTableWidgetItem("Координата Y"))
        self.table.setColumnWidth(0, 150)
        self.table.setColumnWidth(1, 150)

        self.x = QtGui.QLineEdit()
        self.y = QtGui.QLineEdit()

        button_add = QtGui.QPushButton("Добавить", self.centralWidget)
        button_ok = QtGui.QPushButton("Ok",self.centralWidget)
        button_exit = QtGui.QPushButton("Выход", self.centralWidget)
        button_clear = QtGui.QPushButton("Очистить", self.centralWidget)

        self.dxf_radio = QtGui.QRadioButton("DXF", self.centralWidget)
        self.csv_radio = QtGui.QRadioButton("CSV", self.centralWidget)

        layout_text_edit.addWidget(self.x)
        layout_text_edit.addWidget(self.y)
        layout_text_edit.addWidget(button_add)
        layout_vbox.addLayout(layout_text_edit, QtCore.Qt.AlignTop)
        layout_radio.addWidget(self.dxf_radio)
        layout_radio.addWidget(self.csv_radio)
        layout_vbox.addLayout(layout_radio)
        layout_vbox.addWidget(self.table)
        layout_buttons.addWidget(button_clear)
        layout_buttons.addWidget(button_ok)
        layout_buttons.addWidget(button_exit)
        layout_vbox.addLayout(layout_buttons,QtCore.Qt.AlignBottom)

        self.connect(button_add,QtCore.SIGNAL('clicked()'), self.add_coord)
        self.connect(button_ok,QtCore.SIGNAL('clicked()'),self.convert)
    def add_coord(self):
        count = self.table.rowCount()
        if count is None:
            count = 0
        else:
            count += 0
        self.table.insertRow(count)
        self.table.setItem(count, 0, QtGui.QTableWidgetItem(str(self.x.text())))
        self.table.setItem(count, 1, QtGui.QTableWidgetItem(str(self.y.text())))
        self.x.clear()
        self.y.clear()

    def convert(self):
        points = []
        for i in range(0,self.table.rowCount()):
            point_x = self.table.item(i,0).text()
            point_y = self.table.item(i,1).text()
            point = tuple([float(point_x), float(point_y)])
            points.append(point)
        print(points)
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Manual()
    window.show()
    sys.exit(app.exec_())