import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico', 'themes/', 'images/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon.ico"
)

# SETUP CX FREEZE
setup(
    name="TheKitchenProject",
    version="1.0",
    description="Ing. Software Project",
    author="Jesus Jalomo",
    options={'build_exe': {'include_files': files}},
    executables=[target]

)
