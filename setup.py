from cx_Freeze import setup, Executable

setup(name = "locationTracker" ,
      version = "0.1" ,
      description = "" ,
      executables = [Executable("locationTracker.py")])