import sys
from cx_Freeze import setup, Executable

base = "Win32GUI"
executables = {
    Executable('Main.py', includes=['ConvertDXF.py', 'ManualConvert.py'],
               icon='icons\Icons8-Windows-8-Numbers-1-Black.ico')
}
build_exe_options = {
    "base": base,
    "compressed": True,
    "create_shared_zip": True,
    "include_files": [
        "icons\eye.png",
        "icons\gconfeditor.png",
        "icons\\note.png",
        "icons\pen.png",
        "icons\power.png",
        "settings.json",
        "msvcr100.dll"
    ]
}
setup(name="Converter",
      version="0.0.1",
      description="ConvertDXF and stuff like that",
      options={"build_exe": build_exe_options},
      executables=executables,
      )
