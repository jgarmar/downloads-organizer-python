:: Downloads Organizer - Background Process Launcher
:: This script launches the downloads organizer using pythonw.exe (no console window)
:: Uses the Python interpreter from the virtual environment

@echo off
start /B "" "%~dp0venv\Scripts\pythonw.exe" "%~dp0downloads_organizer.py"