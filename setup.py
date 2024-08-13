import os
from cx_Freeze import setup, Executable

# Manually specify the paths for tcl and tk DLLs
tcl_library = r'C:\Users\Dario Gerald\AppData\Local\Programs\Python\Python312\tcl\tcl8.6'
tk_library = r'C:\Users\Dario Gerald\AppData\Local\Programs\Python\Python312\tk\tk8.6'

# Specify the files to include in the build
include_files = [
    ('click_sound.mp3', 'click_sound.mp3'),
    ('clock_icon.png', 'clock_icon.png'),
    ('logo.ico', 'logo.ico'),
    ('pause_icon.png', 'pause_icon.png'),
    ('restart_icon.png', 'restart_icon.png'),
    (tcl_library, 'tcl'),  # Include tcl DLLs
    (tk_library, 'tk'),    # Include tk DLLs
]

setup(
    name="Battletimer",
    version="1.0",
    description="A battle timer application.",
    options={
        "build_exe": {
            "include_files": include_files,
            "packages": ["tkinter", "pygame"],
            "optimize": 2,
        }
    },
    executables=[Executable("main.py", base=None, icon="logo.ico", target_name="Battletimer.exe")],
)
