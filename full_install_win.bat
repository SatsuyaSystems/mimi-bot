@echo off
REM --- Script to setup, clone, and run Mimi-Bot on Windows ---

echo Checking for Python...
REM Check if python command is available
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Python was not found. Please install Python 3 from https://www.python.org/downloads/
    echo Script will continue, but subsequent steps may fail if Python is required.
    echo.
    timeout /t 5 /nobreak >nul
) else (
    echo Python found.
)

echo Checking for Git...
REM Check if git command is available
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Git was not found. Please install Git from https://git-scm.com/downloads
    echo Script will continue, but git clone will fail.
    echo.
    timeout /t 5 /nobreak >nul
) else (
    echo Git found.
)

echo Cloning the repository https://github.com/SatsuyaSystems/mimi-bot.git...

REM Check if the target directory already exists
IF EXIST "mimi-bot" (
    echo Directory "mimi-bot" already exists. Skipping clone.
    echo If you want to re-clone, please delete the "mimi-bot" folder first.
) ELSE (
    REM Perform the git clone command
    git clone https://github.com/SatsuyaSystems/mimi-bot.git
    REM Check if git clone was successful
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Git clone failed. Please check your Git installation and network connection.
        echo Script will exit.
        echo.
        pause
        exit /b %errorlevel%
    )
    echo Repository cloned successfully.
)

echo Navigating into the repository directory...
cd mimi-bot
REM Check if changing directory was successful
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to change directory to "mimi-bot".
    echo Script will exit.
    echo.
    pause
    exit /b %errorlevel%
)
echo Inside mimi-bot directory.

echo Running setup.bat...
REM Execute the setup script
call setup.bat
REM Check if setup.bat was successful
if %errorlevel% neq 0 (
    echo.
    echo WARNING: setup.bat reported an error. Check its output for details.
    echo Script will attempt to continue with start.bat.
    echo.
    timeout /t 5 /nobreak >nul
) else (
    echo setup.bat completed.
)

echo Running start.bat...
REM Execute the start script
call start.bat
REM Check if start.bat was successful
if %errorlevel% neq 0 (
    echo.
    echo WARNING: start.bat reported an error. Check its output for details.
    echo.
    timeout /t 5 /nobreak >nul
) else (
    echo start.bat completed.
)

echo --- Script finished ---

REM Pause to keep the window open
echo.
pause
