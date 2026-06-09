from cx_Freeze import setup, Executable

setup(name="Batch image metadata remover", executables=[Executable("Batch image metadata remover script.py")], options={"build_exe": {"excludes": ["tkinter"]}})