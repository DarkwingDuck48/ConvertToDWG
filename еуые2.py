import ezdxf


dxf = ezdxf.readfile("testFiles\\1часток.dxf")
if dxf.dxfversion == "AC1009":
    print("Old DXF")
else:
    print("New DXF")