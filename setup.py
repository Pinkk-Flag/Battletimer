from cx_Freeze import setup, Executable

# GUID you provided
upgrade_code = "{f456505c-f21c-4225-bd52-524bdf85f060}"

# Specify the files to include in the build
include_files = ['click_sound.mp3', 'clock_icon.png', 'logo.ico', 'pause_icon.png', 'restart_icon.png']

# Setup configuration
setup(
    name="Battletimer",
    version="1.0",
    description="A battle timer application.",
    options={
        "build_exe": {
            "include_files": include_files,
        },
        "bdist_msi": {
            "upgrade_code": upgrade_code
        }
    },
    executables=[Executable("main.py", base=None, icon="logo.ico")]
)
