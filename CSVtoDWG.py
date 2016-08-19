import ezdxf

coords = []
f = open("testFiles/ОКС.csv", "r")
for line in f:
    good_coords = ""
    for char in line:
        if char == ",":
            char = "."
        good_coords += char
    coord = [float(coord) for coord in good_coords.strip().split(";")]
    coords.append(coord)
f.close()
print(coords)

dwg = ezdxf.new("AC1015")
msp = dwg.modelspace()

points = [tuple(coord) for coord in coords]
print(points)
msp.add_lwpolyline(points)

dwg.saveas("icons/testCSV.dxf")