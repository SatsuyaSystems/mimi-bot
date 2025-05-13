@echo off
rem --- Script to update the current Git repository ---

echo Navigating to script directory (if needed)...
:: The '%~dp0' expands to the drive letter and path of the script file.
:: Using this ensures the script runs in its own directory, which should
:: be the root of your Git repo if you place the script there.
:: Remove the 'rem ' at the start of the next line if you want this behaviour.
rem cd /d "%~dp0"

echo Updating the current Git repository using 'git pull'...

:: Perform the git pull command
:: The '-v' flag provides verbose output, which is often helpful.
git pull -v

:: Check the exit code of the git pull command
if %errorlevel% neq 0 (
    echo.
    echo An error occurred during the git pull operation.
    echo Error code: %errorlevel%
    echo Please check the output above for details.
) else (
    echo.
    echo Git pull completed successfully.
)

rem --- Pause to keep the window open after execution ---
echo.