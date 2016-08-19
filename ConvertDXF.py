import json
import os
import sys

from PyQt4 import QtGui, QtCore


class Window(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        with open('settings.json', "r", encoding='utf-8') as file:
            self.settings = json.load(file)
        # Настройка главного окна
        self.setGeometry(400, 300, 280, 250)
        self.setWindowIcon(QtGui.QIcon("icons/gconfeditor.png"))
        self.centralWidget = QtGui.QWidget()
        self.setCentralWidget(self.centralWidget)
        # Верхняя панель меню

        # Опции вкладок
        icon_open = QtGui.QIcon("icons/eye.png")
        menu_open = QtGui.QAction(icon_open, "Open", self)
        menu_open.setShortcut("Ctrl-O")
        menu_open.setStatusTip("Open file")

        icon_exit = QtGui.QIcon("icons/power.png")
        menu_exit = QtGui.QAction(icon_exit, "Exit", self)
        menu_exit.setShortcut("Ctrl-Q")
        menu_open.setStatusTip("Exit application")

        # Сама панель
        menubar = self.menuBar()
        file = menubar.addMenu('&File')
        file.addAction(menu_open)
        file.addSeparator()
        file.addAction(menu_exit)
        # Расположение элементов

        # Слои
        layout_grid = QtGui.QGridLayout()
        vbox = QtGui.QVBoxLayout()
        layout_file = QtGui.QHBoxLayout()
        layout_save = QtGui.QHBoxLayout()
        layout_clear = QtGui.QHBoxLayout()
        layout_save_name = QtGui.QHBoxLayout()
        bottom = QtGui.QHBoxLayout()
        bottom.addStretch(5)
        layout_grid.addLayout(vbox, 100, 100, 3, 2, QtCore.Qt.AlignTop)
        layout_grid.addLayout(bottom, 100, 100, 5, 2, QtCore.Qt.AlignBottom)
        self.centralWidget.setLayout(layout_grid)
        # Элементы

        # Метки
        dialog_label = QtGui.QLabel("Выбор директории")
        list_of_files = QtGui.QLabel("Выбор места сохранения")
        name_label = QtGui.QLabel("Имя сохраняемого файла")

        # Кнопки
        button_open_to_open = QtGui.QPushButton("Open", self.centralWidget)
        button_open_to_save = QtGui.QPushButton("Save", self.centralWidget)
        button_ok = QtGui.QPushButton("Ok", self.centralWidget)
        button_exit = QtGui.QPushButton("Exit", self.centralWidget)
        button_clear = QtGui.QPushButton("Clear", self.centralWidget)

        # Текстовые линии
        self.path_to_file = QtGui.QLineEdit()
        self.path_to_save = QtGui.QLineEdit()
        self.name_file = QtGui.QLineEdit()

        # Версии получаемого DXF файла
        self.dxf_version = QtGui.QComboBox()
        self.versions = {"AutoCAD R12": "AC1009", "AutoCAD R13": "AC1012", "AutoCAD R14": "AC1014",
                         "AutoCAD 2000": "AC1015",
                         "AutoCAD 2004": "AC1018", "AutoCAD 2007": "AC1021", "AutoCAD 2010": "AC1024",
                         "AutoCAD 2013": "AC1027"}
        for key in self.versions.keys():
            self.dxf_version.addItem(key)

        # Компановка
        vbox.addWidget(dialog_label)
        layout_file.addWidget(self.path_to_file)
        layout_file.addWidget(button_open_to_open)
        vbox.addLayout(layout_file)
        vbox.addWidget(list_of_files)
        layout_save.addWidget(self.path_to_save)
        layout_save.addWidget(button_open_to_save)
        layout_save_name.addWidget(self.name_file)
        layout_save_name.addWidget(self.dxf_version)
        vbox.addLayout(layout_save)
        vbox.addWidget(name_label)
        vbox.addLayout(layout_clear)
        vbox.addLayout(layout_save_name)
        bottom.addWidget(button_clear, 200, QtCore.Qt.AlignLeft)
        bottom.addWidget(button_ok)
        bottom.addWidget(button_exit)

        # Соединение функций со кнопками и меню
        self.connect(button_open_to_open, QtCore.SIGNAL('clicked()'), self.openfiledialog)
        self.connect(button_open_to_save, QtCore.SIGNAL('clicked()'), self.openfiledialog)
        self.connect(button_clear, QtCore.SIGNAL('clicked()'), self.cleartext)
        self.connect(menu_open, QtCore.SIGNAL('triggered()'), self.openfiledialog)
        self.connect(menu_exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        self.connect(button_exit, QtCore.SIGNAL('clicked()'), QtCore.SLOT('close()'))
        self.connect(button_ok, QtCore.SIGNAL('clicked()'), self.convert)

    # Функции
    def openfiledialog(self):
        if self.settings['lastdirectory'] == '':
            link = '/home'
        else:
            link = os.path.normpath(self.settings['lastdirectory'])
        if self.sender().text() == "Open":
            filename = QtGui.QFileDialog.getOpenFileName(self.centralWidget, "Open file", link,
                                                         "Файлы CSV (*.csv);;Файлы обмена чертежей AutoCAD(*.dxf)")
            self.path_to_file.setText(filename)
            if filename[-4:] == ".dxf":
                self.dxf_version.setDisabled(True)
        if self.sender().text() == "Save":
            if self.path_to_file.text() == "":
                link = os.path.normpath(self.settings['lastdirectory'])
            else:
                link = os.path.normpath(self.path_to_file.text())
            filename = QtGui.QFileDialog.getExistingDirectory(self.centralWidget, "Save file", link)
            self.path_to_save.setText(filename)
        return link

    def cleartext(self):
        self.path_to_file.clear()
        self.path_to_save.clear()
        self.name_file.clear()

    def convert(self):
        import ezdxf
        path_to_file = os.path.normpath(self.path_to_file.text())
        path_to_save = os.path.normpath(self.path_to_save.text())
        name = self.name_file.text()
        if str(path_to_file)[-4:] == ".csv":
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
            dxf = ezdxf.new(dxfversion=self.versions[key])
            msp = dxf.modelspace()
            points = tuple([coord for coord in coords])
            msp.add_lwpolyline(points)
            dxf.saveas(save_to)
        if str(path_to_file)[-4:] == ".dxf":
            msgBox = QtGui.QMessageBox(self)
            msgBox.question(msgBox,"Не рефлизовано", "Поддержка dxf не реализована")
        self.settings["lastdirectory"] = path_to_file
        with open('settings.json', 'w', encoding='utf-8') as file:
            file.write(json.dumps(self.settings, ensure_ascii=False))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
