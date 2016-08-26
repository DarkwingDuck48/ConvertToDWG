"""
Maxim Britvin, 2016
email: maksbritvin@gmail.com

TODO :
Добавить поддержку txt
"""

import json
import os
import sys
import subprocess

from PyQt4 import QtGui, QtCore
from ezdxf.lldxf.const import DXFStructureError
from ManualConvert import Manual

class Window(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        with open('settings.json', "r", encoding='utf-8') as file:
            self.settings = json.load(file)
        # Настройка главного окна
        self.setGeometry(400, 300, 280, 400)
        self.setWindowIcon(QtGui.QIcon("icons/gconfeditor.png"))
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)

        # Слои
        layout_grid = QtGui.QGridLayout()
        vbox = QtGui.QVBoxLayout()
        layout_file = QtGui.QHBoxLayout()
        layout_save = QtGui.QHBoxLayout()
        layout_clear = QtGui.QHBoxLayout()
        layout_save_name = QtGui.QHBoxLayout()
        layout_settings_dxf = QtGui.QHBoxLayout()
        layout_label = QtGui.QHBoxLayout()
        bottom = QtGui.QHBoxLayout()
        bottom.addStretch(5)
        layout_grid.addLayout(vbox, 100, 100, 3, 2, QtCore.Qt.AlignTop)
        layout_grid.addLayout(bottom, 100, 100, 5, 2, QtCore.Qt.AlignBottom)
        self.centralWidget.setLayout(layout_grid)
        # Элементы

        # Метки
        dialog_label = QtGui.QLabel("Выбор конвертируемого файла")
        list_of_files = QtGui.QLabel("Выбор места сохранения")
        self.name_label = QtGui.QLabel("Имя сохраняемого файла")
        self.name_dxf = QtGui.QLabel("Версия AutoCAD")
        self.name_dxf.setVisible(False)
        self.name_type_line = QtGui.QLabel("Тип добавления")
        self.name_type_line.setVisible(False)

        # Кнопки
        button_open_to_open = QtGui.QPushButton("Open", self.centralWidget)
        button_open_to_save = QtGui.QPushButton("Save", self.centralWidget)
        button_ok = QtGui.QPushButton("Ok", self.centralWidget)
        button_exit = QtGui.QPushButton("Назад", self.centralWidget)
        button_clear = QtGui.QPushButton("Очистить", self.centralWidget)

        # Текстовые линии
        self.path_to_file = QtGui.QLineEdit()
        self.path_to_save = QtGui.QLineEdit()
        self.name_file = QtGui.QLineEdit()

        # Версии получаемого DXF файла
        self.dxf_version = QtGui.QComboBox()
        self.versions = {"AutoCAD R12": "AC1009", "AutoCAD 2000": "AC1015", "AutoCAD 2004": "AC1018",
                         "AutoCAD 2007": "AC1021", "AutoCAD 2010": "AC1024", "AutoCAD 2013": "AC1027"}
        for key in self.versions.keys():
            self.dxf_version.addItem(key)
        self.type_line = QtGui.QComboBox()
        self.type_line.addItems(["Точки", "Линии"])

        self.dxf_version.setVisible(False)
        self.type_line.setVisible(False)

        # Компановка
        vbox.addWidget(dialog_label)
        layout_file.addWidget(self.path_to_file)
        layout_file.addWidget(button_open_to_open)
        vbox.addLayout(layout_file)
        vbox.addWidget(list_of_files)
        layout_save.addWidget(self.path_to_save)
        layout_save.addWidget(button_open_to_save)
        layout_save_name.addWidget(self.name_file)
        layout_label.addWidget(self.name_dxf)
        layout_label.addWidget(self.name_type_line)
        vbox.addLayout(layout_save)
        vbox.addWidget(self.name_label)
        layout_settings_dxf.addWidget(self.dxf_version)
        layout_settings_dxf.addWidget(self.type_line)
        vbox.addLayout(layout_clear)
        vbox.addLayout(layout_save_name)
        vbox.addLayout(layout_label)
        vbox.addLayout(layout_settings_dxf)
        bottom.addWidget(button_clear, 200, QtCore.Qt.AlignLeft)
        bottom.addWidget(button_ok)
        bottom.addWidget(button_exit)

        # Соединение функций со кнопками и меню

        self.connect(button_open_to_open, QtCore.SIGNAL('clicked()'), self.openfiledialog)
        self.connect(button_open_to_save, QtCore.SIGNAL('clicked()'), self.openfiledialog)
        self.connect(button_clear, QtCore.SIGNAL('clicked()'), self.cleartext)
        self.connect(button_exit, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        self.connect(button_ok, QtCore.SIGNAL('clicked()'), self.convert)

    # Функции
    def openfiledialog(self):
        if self.settings['lastdirectory'] == '':
            link = '/home'
        else:
            link = os.path.normpath(self.settings['lastdirectory'])
        if self.sender().text() == "Открыть файл" or self.sender().text() == "Open":
            filename = QtGui.QFileDialog.getOpenFileName(self.centralWidget, "Open file", link,
                                                         "Файлы CSV (*.csv);;Файлы обмена чертежей AutoCAD(*.dxf);; "
                                                         "Текстовые файлы (*txt)")
            self.path_to_file.setText(filename)
            if filename[-4:] == ".dxf":
                self.dxf_version.setVisible(False)
                self.type_line.setVisible(False)
                self.name_dxf.setVisible(False)
                self.name_type_line.setVisible(False)
            if filename[-4:] == ".csv" or filename[-4:] == ".txt":
                self.dxf_version.setVisible(True)
                self.type_line.setVisible(True)
                self.name_dxf.setVisible(True)
                self.name_type_line.setVisible(True)
        if self.sender().text() == "Save":
            if self.path_to_file.text() == "":
                link = os.path.normpath(self.settings['lastdirectory'])
            else:
                link = os.path.normpath(self.path_to_file.text())
            filename = QtGui.QFileDialog.getExistingDirectory(self.centralWidget, "Save file", link)
            self.path_to_save.setText(filename)

    def cleartext(self):
        self.path_to_file.clear()
        self.path_to_save.clear()
        self.name_file.clear()

    def convert(self):
        import ezdxf
        # Получение необходимых данных из формы

        path_to_file = os.path.normpath(self.path_to_file.text())
        path_to_save = os.path.normpath(self.path_to_save.text())
        name = self.name_file.text()
        import_type = self.type_line.itemText(self.type_line.currentIndex())

        # Обработка, если исходный файл с расширением .csv
        if str(path_to_file)[-4:] == ".csv" or str(path_to_file)[-4] == ".txt":
            save_to = os.path.normpath(path_to_save + '\\' + name + ".dxf")
            key = self.dxf_version.itemText(self.dxf_version.currentIndex())
            coords = []
            with open(path_to_file, 'r') as csv:
                for line in csv:
                    good_coord = ''
                    for char in line:
                        if char == ',':
                            char = '.'
                        good_coord += char
                    coord = [float(coord) for coord in good_coord.strip().split(";")]
                    coords.append(coord)

            points = tuple([coord for coord in coords])
            # Вывод в старые версии Autocad (R12)
            if self.versions[key] == "AC1009":
                from ezdxf.r12writer import r12writer
                with r12writer(str(save_to)) as dxf:
                    if import_type == "Линии":
                        dxf.add_polyline(points)
                    else:
                        for point in points:
                            dxf.add_point(point)

            # Вывод в новые версии Autocad
            else:
                dxf = ezdxf.new(dxfversion=self.versions[key])
                msp = dxf.modelspace()
                if import_type == "Линии":
                    msp.add_lwpolyline(points)
                else:
                    for point in points:
                        msp.add_point(point)
                dxf.saveas(save_to)
            subprocess.Popen('explorer %s' % path_to_save)

        # Обработка, если исходный файл с расширением .dxf
        if str(path_to_file)[-4:] == ".dxf":
            try:
                dxf = ezdxf.readfile(path_to_file)
                msp = dxf.modelspace()
            except DXFStructureError:
                error = QtGui.QErrorMessage()
                error.showMessage("Произошла ошибка при открытии файла %s" % path_to_file)

            if dxf.dxfversion == "AC1009":
                polyline = list(msp.querry("POLYLINE"))
            else:
                polyline = list(msp.query("LWPOLYLINE"))

            if len(polyline) > 1:
                path_to_convert = os.path.normpath(path_to_save +"\\"+name+"_converted")
                os.mkdir(path_to_convert)
                i = 0
                while i < len(polyline):
                    with open(path_to_convert + "\\" + name + "_" + str(i) + ".csv", "w") as conv:
                        for point in polyline[i]:
                            x = round(point[0], 2)
                            y = round(point[1], 2)
                            conv.write(str(x) + ";" + str(y) + "\n")
                    i += 1
                subprocess.Popen('explorer %s' % path_to_convert)
            elif len(polyline) == 1:
                with open(path_to_save +"\\"+ name + "_converted.csv", "w") as conv:
                    for point in polyline[0]:
                        x = round(point[0], 2)
                        y = round(point[1], 2)
                        conv.write(str(x) + ";" + str(y) + "\n")
                subprocess.Popen('explorer %s' % path_to_save)
            elif len(polyline) == 0:
                msgBox = QtGui.QMessageBox()
                msgBox.question(msgBox, "Внимание!", "На чертеже отсутствуют полилинии!", msgBox.Ok)

        self.settings["lastdirectory"] = path_to_save
        with open('settings.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.settings, ensure_ascii=False))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())