from cx_Freeze import setup, Executable

setup(
    name = "notepad",
    version = "0.1",
    description = "Blackjack",
    executables = [Executable("updater.py")])
