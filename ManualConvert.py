"""
Maxim Britvin, 2016
email: maksbritvin@gmail.com

TODO:
В момент нажатия кнопки OK - открывается окно выбора места сохранения файла.
"""

import os
import sys
import json
import subprocess
from PyQt4 import QtGui, QtCore


class Manual(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Manual, self).__init__(parent)

        with open('settings.json', "r", encoding='utf-8') as file:
            self.settings = json.load(file)
        # Настройка главного окна
        self.setGeometry(400, 300, 361, 454)
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)
        self.setWindowTitle("Ручной ввод")

        layout_grid = QtGui.QGridLayout()
        layout_vbox = QtGui.QVBoxLayout()
        layout_text_edit = QtGui.QHBoxLayout()
        layout_radio = QtGui.QHBoxLayout()
        layout_buttons = QtGui.QHBoxLayout()
        self.layout_settings = QtGui.QHBoxLayout()
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

        self.dxf_version = QtGui.QComboBox()
        self.versions = {"AutoCAD R12": "AC1009", "AutoCAD 2000": "AC1015", "AutoCAD 2004": "AC1018",
                         "AutoCAD 2007": "AC1021", "AutoCAD 2010": "AC1024", "AutoCAD 2013": "AC1027"}
        for key in self.versions.keys():
            self.dxf_version.addItem(key)
        self.type_line = QtGui.QComboBox()
        self.type_line.addItems(["Точки","Линии"])
        self.csv_separator = QtGui.QComboBox()
        self.csv_separator.addItems([";",","])

        self.dxf_version.setVisible(False)
        self.type_line.setVisible(False)
        self.csv_separator.setVisible(False)

        layout_text_edit.addWidget(self.x)
        layout_text_edit.addWidget(self.y)
        layout_text_edit.addWidget(button_add)
        layout_vbox.addLayout(layout_text_edit, QtCore.Qt.AlignTop)
        layout_radio.addWidget(self.dxf_radio)
        layout_radio.addWidget(self.csv_radio)
        layout_vbox.addLayout(layout_radio)
        layout_vbox.addWidget(self.table)
        self.layout_settings.addWidget(self.dxf_version)
        self.layout_settings.addWidget(self.type_line)
        self.layout_settings.addWidget(self.csv_separator)
        layout_vbox.addLayout(self.layout_settings)
        layout_buttons.addWidget(button_clear)
        layout_buttons.addWidget(button_ok)
        layout_buttons.addWidget(button_exit)
        layout_vbox.addLayout(layout_buttons,QtCore.Qt.AlignBottom)

        self.connect(button_add,QtCore.SIGNAL('clicked()'), self.add_coord)
        self.connect(button_ok,QtCore.SIGNAL('clicked()'),self.convert)
        self.connect(self.dxf_radio, QtCore.SIGNAL('clicked()'), self.settings_for_dxf)
        self.connect(self.csv_radio, QtCore.SIGNAL('clicked()'),self.settings_for_csv)

    def add_coord(self):
        count = self.table.rowCount()
        if count is None:
            count = 0
        else:
            count += 0
        self.table.insertRow(count)
        self.table.setRowHeight(count, 20)
        self.table.setItem(count, 0, QtGui.QTableWidgetItem(str(self.x.text())))
        self.table.setItem(count, 1, QtGui.QTableWidgetItem(str(self.y.text())))
        self.x.clear()
        self.y.clear()

    def convert(self):
        points = []
        if self.settings['lastdirectory'] == '':
            link = '/home'
        else:
            link = os.path.normpath(self.settings['lastdirectory'])

        for i in range(0,self.table.rowCount()):
            point_x = self.table.item(i,0).text()
            point_y = self.table.item(i,1).text()
            point = tuple([float(point_x), float(point_y)])
            points.append(point)
        if self.dxf_radio.isChecked():
            filename = QtGui.QFileDialog.getSaveFileName(self.centralWidget, "Сохранить как", link,
                                                         "Файлы обмена чертежей AutoCAD(*.dxf)")
            key = self.dxf_version.itemText(self.dxf_version.currentIndex())
            type_line = self.type_line.itemText(self.type_line.currentIndex())

            if self.versions[key] == "AC1009":
                from ezdxf.r12writer import r12writer
                with r12writer(str(filename)) as dxf:
                    if type_line == "Линии":
                        dxf.add_polyline(points)
                    else:
                        for point in points:
                            dxf.add_point(point)
            else:
                import ezdxf
                dxf = ezdxf.new(dxfversion=self.versions[key])
                msp = dxf.modelspace()
                if type_line == "Линии":
                    msp.add_lwpolyline(points)
                else:
                    for point in points:
                        msp.add_point(point)
                dxf.saveas(filename)
            subprocess.Popen('explorer %s' % os.path.normpath(os.path.dirname(filename)))
        elif self.csv_radio.isChecked():
            filename = QtGui.QFileDialog.getSaveFileName(self.centralWidget, "Сохранить как", link,
                                                         "Файлы CSV (*.csv);;Текстовые файлы(*txt)")
            separator = self.csv_separator.itemText(self.csv_separator.currentIndex())
            with open(filename,'w') as file:
                for point in points:
                    x,y = point
                    file.write(str(x)+separator+str(y)+"\n")
            subprocess.Popen('explorer %s' % os.path.normpath(os.path.dirname(filename)))



    def settings_for_dxf(self):
        self.dxf_version.setVisible(True)
        self.type_line.setVisible(True)
        self.csv_separator.setVisible(False)

    def settings_for_csv(self):
        self.dxf_version.setVisible(False)
        self.type_line.setVisible(False)
        self.csv_separator.setVisible(True)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Manual()
    window.show()
    sys.exit(app.exec_())