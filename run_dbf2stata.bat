@echo off
setlocal
where dbf2stata >nul 2>nul
if %ERRORLEVEL%==0 (
    dbf2stata
) else (
    echo dbf2stata is not installed as a command.
    echo Install it first with: py -m pip install dbf2stata
)
echo.
pause
