@echo off
cd /d %~dp0
call venv\Scripts\activate.bat

echo Running cleanup...
python cleanup.py
if %ERRORLEVEL% NEQ 0 (
    echo Cleanup failed with error code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

echo Running scraper...
python scraper.py
if %ERRORLEVEL% NEQ 0 (
    echo Scraper failed with error code %ERRORLEVEL%
    pause
    exit /b %ERRORLEVEL%
)

deactivate
echo All tasks completed successfully 