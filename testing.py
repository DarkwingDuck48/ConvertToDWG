import ezdxf
import os


path_to_file = os.path.normpath("D:\Проекты\Мой проект\DXFtest\Соловьевка.dxf")
dxf = ezdxf.readfile(path_to_file)
msp = dxf.modelspace()
for e in dxf.entities:
    print("DXF type: %s" % e.dxftype())
