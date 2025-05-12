@echo off
REM Erstellt die virtuelle Umgebung, falls sie nicht existiert
IF NOT EXIST "venv" (
    python -m venv venv
)

REM Aktiviert die virtuelle Umgebung
call venv\Scripts\activate

REM Installiert die Abhängigkeiten
pip install -r requirements.txt

REM Installiert Playwright
playwright install

REM Führt das Python-Skript aus
python main.py

REM Hält das Fenster offen, falls ein Fehler auftritt
pause