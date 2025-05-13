@echo off
REM Lade update.bat
echo Updating the current Git repository using 'git pull'...

:: Perform the git pull command
:: The '-v' flag provides verbose output, which is often helpful.
git pull -v

REM Aktiviert die virtuelle Umgebung
call venv\Scripts\activate

REM Führt das Python-Skript aus
python main.py

REM Hält das Fenster offen, falls ein Fehler auftritt
pause