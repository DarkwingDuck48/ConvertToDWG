"""
!!!! В основную программу входит в тестовом режиме!!!!!
Нет четкой серилизации у XML файлов, формируемых Object-land. Нужны тестовые файлы различных образцов
Не тестированна работа с несколькими объектами в файле.
"""

from bs4 import BeautifulStoneSoup
import ezdxf

xml = open("testFiles\kv_82b85e91-d976-4cf9-b764-e8898001e483.xml", "r", encoding="utf-8")
#xml = open("testFiles\kv_c18abd22-c26e-47e0-a7f2-6a8c76faf891.xml", "r", encoding="utf-8")
soup = BeautifulStoneSoup(xml, features="xml", from_encoding="utf-8")
coords = soup.find_all("Ordinate")
numbers = soup.find_all("SpelementUnit")
points = []
for i in range(0,len(coords)):
    print("{} : X= {}, Y= {}".format(numbers[i]["SuNmb"], coords[i]["X"], coords[i]["Y"]))
    points.append(tuple([float(coords[i]["Y"]),float(coords[i]["X"])]))
print(points)
if points:
    dwg = ezdxf.new("AC1024")
    msp = dwg.modelspace()
    msp.add_lwpolyline(points)
    dwg.saveas("testXML.dxf")
else:
    error = soup.find_all("SpecialNote")
    print(str(error)[14:114])