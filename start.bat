@echo off
REM Aktiviert die virtuelle Umgebung
call venv\Scripts\activate

REM Führt das Python-Skript aus
python gemini.py

REM Hält das Fenster offen, falls ein Fehler auftritt
pause