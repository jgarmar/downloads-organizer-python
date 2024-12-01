@echo off
cd %~dp0
call venv\Scripts\activate
python downloads_organizer.py
pause